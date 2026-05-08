"""
ANALYSIS ENGINE (analyser.py)
----------------------------
This is the "brain" of the application. It compares the user's CV
against job listings to calculate a score and give advice.

How it works:
1. Extract skills from the CV using spaCy (AI)
2. Extract skills from real job listings
3. Compare them to find matches and gaps
4. Calculate a score and generate recommendations
"""

import logging
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)

# --- HELPER FUNCTIONS ---

def _score_to_grade(score):
    """Convert a 0-100 score into a helpful sentence the user can understand."""
    if score >= 85: return "Excellent match! Your CV is very strong."
    if score >= 65: return "Good match. You have most of the key skills."
    if score >= 45: return "Fair match. There are some important gaps to fill."
    if score >= 25: return "Needs work. You're missing many core skills."
    return "Getting started. You need to add more skills to your CV."

def _calculate_salary_insight(jobs):
    """Find the average salary range from the jobs we found.
    
    Goes through all job listings, collects the minimum and maximum salaries,
    and returns the average of each. This gives the user a realistic expectation.
    """
    # Collect all minimum salaries that exist (some jobs don't list salary)
    mins = [j.get("minimumSalary") for j in jobs if j.get("minimumSalary")]
    maxs = [j.get("maximumSalary") for j in jobs if j.get("maximumSalary")]

    if not mins or not maxs:  # If no salary data was found, return nothing
        return None

    return {
        "avg_min": round(sum(mins) / len(mins)),  # Average of all minimum salaries
        "avg_max": round(sum(maxs) / len(maxs)),  # Average of all maximum salaries
        "count": len(mins)  # How many jobs had salary info
    }

def _build_job_skill_frequency(jobs):
    """Count how often each skill appears across all job listings.
    
    For example, if 'Python' appears in 8 out of 10 jobs, its frequency is 80%.
    This tells us which skills employers care about most.
    """
    from collections import Counter
    from .skill_extractor import extract_skills_from_text
    
    counts = Counter()  # A special dictionary that counts things
    for job in jobs:
        # Combine the job title and description into one text block
        text = f"{job.get('jobTitle')} {job.get('jobDescription')}"
        # Use AI to extract skill names from this text
        skills = extract_skills_from_text(text)
        for s in skills:
            counts[s] += 1  # Add 1 every time we see this skill
    
    # Convert counts to percentages (e.g. 8 out of 10 = 80%)
    total = len(jobs)
    return {s: (count / total) * 100 for s, count in counts.items()}


# --- MAIN ANALYSIS PROCESS ---

def analyse(cv_text, cv_sections, jobs, job_title, filename, location=""):
    """
    The main analysis pipeline — this runs when the user clicks 'Analyse'.
    
    Parameters:
        cv_text: The full text extracted from the CV file
        cv_sections: The CV text split into sections (Skills, Experience, etc.)
        jobs: List of real job listings from Reed API
        job_title: What job the user is looking for (e.g. 'Software Engineer')
        filename: Name of the uploaded CV file
        location: Optional city/location filter
    
    Returns:
        A dictionary with everything needed for the results page
    """
    from .skill_extractor import extract_skills_weighted, extract_keywords
    from .skills_data import LEARNING_RESOURCES

    # Step 1: Get skills from the user's CV using AI
    cv_skill_weights = extract_skills_weighted(cv_sections)
    cv_skills = set(cv_skill_weights.keys())  # Just the skill names as a set
    cv_keywords = extract_keywords(cv_text, top_n=15)  # General keywords for recommendations

    # Step 2: Get skills from all the job listings
    job_skill_freq = _build_job_skill_frequency(jobs)  # {skill: frequency%}
    all_required_skills = set(job_skill_freq.keys())  # All unique skills employers want

    # Step 3: Compare CV skills vs job skills
    matched = cv_skills & all_required_skills  # Skills on CV that employers want (intersection)
    missing_names = all_required_skills - cv_skills  # Skills employers want but CV doesn't have

    # Step 4: Calculate the Score (what percentage of required skills does the user have?)
    if all_required_skills:
        score = round((len(matched) / len(all_required_skills)) * 100)
    else:
        score = 0  # No skills found in job listings
    
    score = min(100, score)  # Cap at 100 (can't score more than 100%)
    grade = _score_to_grade(score)  # Convert number to a sentence

    # Step 5: Build the list of missing skills with learning links
    missing_list = []
    # Sort by frequency (most wanted skills first)
    for s in sorted(missing_names, key=lambda x: job_skill_freq.get(x, 0), reverse=True):
        freq = round(job_skill_freq.get(s, 0))
        # High priority = appears in more than 50% of jobs
        priority = "High" if freq > 50 else ("Medium" if freq > 20 else "Low")
        
        missing_list.append({
            "skill": s,
            "frequency": freq,  # What % of jobs ask for this skill
            "priority": priority,  # High, Medium, or Low
            "resources": LEARNING_RESOURCES.get(s, [])  # Free course links
        })

    # Step 6: Calculate match percentage for each individual job listing
    from .skill_extractor import extract_skills_from_text as extract
    enriched_jobs = []
    for job in jobs:
        # Get skills from this specific job
        j_skills = extract(f"{job.get('jobTitle')} {job.get('jobDescription')}")
        m = cv_skills & j_skills  # Which of the user's skills match this job
        pct = round((len(m) / len(j_skills)) * 100) if j_skills else 0
        
        enriched_jobs.append({
            **job,  # Keep all original job data
            "match_pct": pct,  # How well the CV matches THIS specific job
            "matched_tags": sorted(list(m))[:5],  # Top 5 matched skills
            "missing_tags": sorted(list(j_skills - cv_skills))[:5]  # Top 5 missing
        })
    enriched_jobs.sort(key=lambda x: x["match_pct"], reverse=True)  # Best matches first

    # Step 7: Generate actionable recommendations
    recs = []
    if missing_list:
        top = missing_list[0]["skill"].title()  # The most important missing skill
        recs.append({
            "title": f"✏️ Add {top} to your CV",
            "body": f"This skill appears in {missing_list[0]['frequency']}% of jobs. Adding it to your skills section will help you pass ATS filters."
        })
    recs.append({
        "title": "📏 Formatting Tip",
        "body": "Use a simple, one-column layout to make your CV easier for companies to read automatically."
    })

    # Step 8: Run extra analysis features
    from .cv_reviewer import review_cv  # Checks CV quality (contact info, sections, etc.)
    from .job_title_suggester import suggest_alternative_titles  # Suggests other matching roles
    from .interview_prep import generate_interview_questions  # Creates interview questions
    from .linkedin_grader import grade_linkedin_profile  # LinkedIn optimisation tips

    # Return everything the results page needs
    return {
        "filename": filename,
        "job_title": job_title,
        "location": location,
        "score": score,
        "grade": grade,
        "matched": sorted(list(matched)),  # Skills the user has
        "missing": missing_list,  # Skills the user needs
        "jobs": enriched_jobs,  # Job listings with match percentages
        "recommendations": recs,  # Actionable advice
        "cv_review": review_cv(cv_text, cv_sections),  # CV quality check
        "alt_titles": suggest_alternative_titles(cv_skills, job_title),  # Alternative job suggestions
        "salary_insight": _calculate_salary_insight(jobs),  # Average salary range
        "interview_prep": generate_interview_questions(job_title, missing_list),  # Interview questions
        "linkedin_advice": grade_linkedin_profile(job_title, matched, missing_list),  # LinkedIn tips
        "cv_keywords": [kw for kw, _ in cv_keywords],  # General keywords found on CV
        "job_count": len(jobs),  # How many jobs were analysed
        "skills_match_pct": score,  # Same as score (for the progress bar)
        "exp_relevance_pct": 80,  # Placeholder for experience relevance
        "format_pct": 90  # Placeholder for format quality
    }
