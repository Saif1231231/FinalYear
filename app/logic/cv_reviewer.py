"""
CV REVIEWER (cv_reviewer.py)
---------------------------
This file looks at the "quality" of the CV. 
It checks for things like:
- Is there an email and phone number?
- Is it the right length?
- Does it use strong "action words" (like 'Achieved', 'Built')?
- Are there any mistakes in the structure?
"""

import re
import logging

logger = logging.getLogger(__name__)

# --- SETTINGS & DATA ---

# Ideal order for a CV
IDEAL_ORDER = ["SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"]

# Good words to use in a CV
STRONG_WORDS = {'achieved', 'built', 'created', 'delivered', 'designed', 'developed', 'led', 'managed'}

# Weak words to avoid
WEAK_WORDS = ['responsible for', 'helped with', 'worked on', 'team player', 'hardworking']

# Patterns to find contact info
CONTACT_INFO = {
    'email':    re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
    'phone':    re.compile(r'(\+?\d[\d\s\-().]{7,}\d)'),
    'linkedin': re.compile(r'linkedin\.com/in/[\w-]+', re.I),
}

def _check_basics(text, sections):
    """Check for essential items like contact info and sections."""
    results = []
    
    # 1. Contact Info
    has_email = bool(CONTACT_INFO['email'].search(text))
    has_phone = bool(CONTACT_INFO['phone'].search(text))
    results.append({
        "label": "Contact Details",
        "status": "pass" if (has_email and has_phone) else "warn",
        "detail": "Found email and phone." if (has_email and has_phone) else "Missing email or phone number."
    })

    # 2. Key Sections
    for s in ["SUMMARY", "SKILLS", "EXPERIENCE"]:
        found = s in sections
        results.append({
            "label": f"{s.title()} Section",
            "status": "pass" if found else "fail",
            "detail": f"{s.title()} section is present." if found else f"Please add a {s.title()} section."
        })

    return results

def _get_suggestions(text, sections):
    """Generate advice on how to improve the CV content."""
    advice = []
    text_lower = text.lower()

    # Check word count
    word_count = len(text.split())
    if word_count < 300:
        advice.append({"category": "Length", "title": "CV is too short", "body": "Add more detail about your projects and experience.", "severity": "high"})
    elif word_count > 1000:
        advice.append({"category": "Length", "title": "CV is too long", "body": "Try to keep your CV under 2 pages (approx 800 words).", "severity": "medium"})

    # Check for action words
    found_strong = [w for w in STRONG_WORDS if w in text_lower]
    if len(found_strong) < 3:
        advice.append({"category": "Writing", "title": "Use stronger verbs", "body": "Use words like 'Achieved' or 'Managed' to describe your work.", "severity": "medium"})

    # Check for weak words
    found_weak = [w for w in WEAK_WORDS if w in text_lower]
    if found_weak:
        advice.append({"category": "Writing", "title": "Remove generic phrases", "body": f"Avoid using phrases like '{found_weak[0]}'. Be more specific.", "severity": "low"})

    return advice

def review_cv(text, sections):
    """
    Main function: Runs all checks and gives the CV a final grade.
    """
    checklist = _check_basics(text, sections)
    suggestions = _get_suggestions(text, sections)
    
    # Calculate a simple grade based on how many checks passed
    passes = sum(1 for c in checklist if c['status'] == 'pass')
    score = (passes / len(checklist)) * 100
    
    if score >= 80: grade = "A"
    elif score >= 60: grade = "B"
    elif score >= 40: grade = "C"
    else: grade = "D"

    return {
        "grade": grade,
        "grade_description": f"Overall Quality Grade: {grade}",
        "checklist": checklist,
        "suggestions": suggestions,
        "word_count": len(text.split()),
        "pass_count": passes,
        "total_checks": len(checklist)
    }
