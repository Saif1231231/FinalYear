"""
SKILL EXTRACTOR (skill_extractor.py)
------------------------------------
This is the AI-powered module that reads text and finds skill names in it.
It uses three methods (layers) to make sure it catches as many skills as possible:

Layer 1 — Regex: Searches for exact skill phrases like "machine learning" or "node.js"
Layer 2 — spaCy NLP: Uses AI to understand word meanings (e.g. "developing" = "develop")
Layer 3 — Synonyms: Maps different names for the same skill ("reactjs" = "react")

This file also gives extra weight to skills found in the "Skills" section vs other sections.
"""

import re
import logging
from collections import Counter
from typing import Set, Dict, List, Tuple

logger = logging.getLogger(__name__)

# The AI model is loaded only once to save memory (lazy loading)
_nlp = None


def _get_nlp():
    """Load the spaCy English language model (only once, the first time it's needed)."""
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")  # Small English model (~12MB)
            logger.info("spaCy model loaded")
        except OSError:
            logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise
    return _nlp


# ── Layer 1: Regex Phrase Matching ──
# This catches multi-word skills like "machine learning", "node.js", "c++", "ci/cd"

def _match_phrases(text: str, skill_list: List[str]) -> Set[str]:
    """Search for exact skill names in the text using pattern matching.
    
    For example, if the text says "I know machine learning", this will find "machine learning".
    It handles special characters like dots (node.js) and plus signs (c++).
    """
    text_lower = text.lower()
    found = set()
    for skill in skill_list:
        # Build a search pattern with word boundaries so "java" doesn't match "javascript"
        escaped = re.escape(skill)
        pattern = r'(?<![a-zA-Z0-9])' + escaped + r'(?![a-zA-Z0-9])'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


# ── Layer 2: spaCy AI Matching ──
# This uses Natural Language Processing to understand variations of words

def _match_lemmas(text: str, skill_set: set) -> Set[str]:
    """Use spaCy AI to find skills even when written differently.
    
    For example, "developing" becomes "develop" (lemmatisation).
    Also checks pairs of words (bigrams) like "data" + "science" = "data science".
    """
    found = set()
    try:
        nlp = _get_nlp()
        doc = nlp(text[:50_000])  # Limit to 50k characters for speed

        tokens = list(doc)
        for i, token in enumerate(tokens):
            lemma = token.lemma_.lower().strip()  # Get the base form of the word

            # Check if this single word matches a skill
            if lemma in skill_set:
                found.add(lemma)

            # Check if this word + next word together match a skill
            if i < len(tokens) - 1:
                bigram = lemma + " " + tokens[i + 1].lemma_.lower().strip()
                if bigram in skill_set:
                    found.add(bigram)

    except Exception as e:
        logger.warning("spaCy lemma pass failed: %s", e)
    return found


# ── Layer 3: Synonym Normalisation ──
# Maps different names for the same skill to one standard name

def _normalise_synonyms(skill_set: Set[str], synonyms: dict) -> Set[str]:
    """Convert skill aliases to their standard name.
    
    For example: "reactjs" → "react", "sklearn" → "scikit-learn"
    """
    return {synonyms.get(s, s) for s in skill_set}


# ── General Keyword Extraction (for recommendations) ──

def extract_keywords(text: str, top_n: int = 30) -> List[Tuple[str, int]]:
    """Extract the most common meaningful words from text using spaCy.
    
    Unlike skill extraction, this finds ANY important words (not just from our skills list).
    Used for building additional recommendations and CV keyword analysis.
    Returns a list of (word, count) sorted by how often each word appears.
    """
    try:
        nlp = _get_nlp()
        doc = nlp(text[:80_000])

        # Common words to ignore (they appear everywhere and aren't useful)
        stopwords = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'she',
            'it', 'its', 'they', 'them', 'what', 'which', 'who', 'this', 'that',
            'are', 'was', 'is', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'into', 'through', 'during',
            'including', 'until', 'against', 'among', 'throughout', 'experience',
            'work', 'also', 'both', 'each', 'more', 'most', 'other', 'some',
            'responsible', 'responsibility', 'role', 'position', 'candidate',
            'employer', 'employee', 'client', 'team', 'member', 'department',
            'ability', 'strong', 'excellent', 'good', 'great', 'key', 'use',
            'using', 'used', 'based', 'within', 'across', 'ensure', 'support'
        }

        counts = Counter()

        # Find named entities (company names, product names, locations)
        for ent in doc.ents:
            if ent.label_ in {'ORG', 'PRODUCT', 'GPE', 'NORP', 'TECH'}:
                kw = ent.text.lower().strip()
                if len(kw) > 2 and kw not in stopwords:
                    counts[kw] += 2  # Named entities get double weight

        # Find noun phrases (e.g. "software development", "data analysis")
        for chunk in doc.noun_chunks:
            kw = chunk.root.lemma_.lower().strip()
            if len(kw) > 3 and kw not in stopwords and kw.isalpha():
                counts[kw] += 1

        return counts.most_common(top_n)  # Return the top N most common keywords

    except Exception as e:
        logger.warning("Keyword extraction failed: %s", e)
        return []


# ── Main Skill Extraction Function ──

def extract_skills_from_text(text: str) -> Set[str]:
    """Extract skills from any text using all three layers.
    
    This is the main function used throughout the project. Give it any text
    (a CV, a job description, etc.) and it returns a set of skill names found.
    """
    from .skills_data import ALL_SKILLS, SYNONYMS

    if not text or len(text.strip()) < 20:  # Skip if text is too short
        return set()

    # Layer 1: Find exact skill phrases using regex
    found = _match_phrases(text, ALL_SKILLS)

    # Layer 2: Find skills using AI lemmatisation
    skill_set = set(ALL_SKILLS)
    found |= _match_lemmas(text, skill_set)  # |= means "add to the existing set"

    # Layer 3: Normalise synonyms (e.g. "reactjs" → "react")
    found = _normalise_synonyms(found, SYNONYMS)

    logger.info("Extracted %d skills from %d chars", len(found), len(text))
    return found


def extract_skills_weighted(sections: dict) -> Dict[str, float]:
    """Extract skills from a CV that's been split into sections, with weighting.
    
    Skills found in the "Skills" section get a higher weight (2.0) because
    the user explicitly listed them. Skills in "Experience" get 1.5 because
    they were mentioned in context. Other sections get 1.0.
    
    Returns a dictionary like: {"python": 2.0, "react": 1.5, "git": 1.0}
    """
    from .skills_data import ALL_SKILLS, SYNONYMS

    # How much weight each section gets
    SECTION_WEIGHTS = {
        'SKILLS':         2.0,  # User explicitly listed this skill
        'CERTIFICATIONS': 2.0,  # They have a certificate for it
        'EXPERIENCE':     1.5,  # They used it at work
        'PROJECTS':       1.3,  # They built something with it
        'EDUCATION':      1.0,  # Learned it at university
        'SUMMARY':        1.0,  # Mentioned it briefly
        'OTHER':          1.0,  # Found somewhere else on the CV
    }

    skill_weights: Dict[str, float] = {}

    for section_name, section_text in sections.items():
        weight = SECTION_WEIGHTS.get(section_name, 1.0)  # Get the weight for this section
        # Run all three extraction layers on this section
        skills_in_section = _match_phrases(section_text, ALL_SKILLS)
        skills_in_section |= _match_lemmas(section_text, set(ALL_SKILLS))
        skills_in_section = _normalise_synonyms(skills_in_section, SYNONYMS)

        for skill in skills_in_section:
            # Keep the highest weight if a skill appears in multiple sections
            skill_weights[skill] = max(skill_weights.get(skill, 0), weight)

    return skill_weights


def skills_to_categories(skill_set: Set[str]) -> dict:
    """Group skills into their categories (e.g. "python" → "Programming Languages").
    
    Used for display purposes on the results page.
    Returns: {"Programming Languages": ["python", "java"], "Databases": ["sql"]}
    """
    from .skills_data import SKILLS
    result = {}
    for category, skill_list in SKILLS.items():
        matched = [s for s in skill_list if s in skill_set]
        if matched:
            result[category] = matched
    return result
