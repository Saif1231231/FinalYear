"""
LINKEDIN GRADER (linkedin_grader.py)
-----------------------------------
This file generates a simple checklist of advice for the user's LinkedIn profile.
It uses the job title they searched for and the skills found on their CV 
to suggest exactly what they should put on their LinkedIn page.
"""

def grade_linkedin_profile(job_title, matched_skills, missing_skills):
    """
    Returns a list of LinkedIn optimization tips to display on the results page.
    """
    tips = []

    # 1. Headline Tip
    # Takes the top 3 skills they have and suggests a headline.
    top_matched = [s.title() for s in list(matched_skills)[:3]]
    tips.append({
        "label": "Headline Optimisation",
        "detail": f"Update your headline to: 'Aspiring {job_title} | Proficient in {', '.join(top_matched)}'",
        "status": "info"
    })

    # 2. About Section Keywords Tip
    # Suggests putting their top 5 skills in the About section.
    about_keywords = [s.title() for s in list(matched_skills)[:5]]
    tips.append({
        "label": "About Section Keywords",
        "detail": f"Ensure your 'About' section contains the keywords: {', '.join(about_keywords)}. This helps LinkedIn's internal search algorithm find you.",
        "status": "pass"
    })

    # 3. Skills Section Tip
    # Reminds them to add their top missing skill to LinkedIn once they learn it.
    if missing_skills:
        top_missing = missing_skills[0]['skill'].title()
        tips.append({
            "label": "Skills & Endorsements",
            "detail": f"Add {top_missing} to your skills section. Once you complete the course on your Learning Path, ask a colleague for an endorsement.",
            "status": "warn"
        })

    # 4. Profile Photo Tip
    tips.append({
        "label": "Professional Branding",
        "detail": "Use a professional headshot and a custom background banner related to tech or your specific industry to look more established.",
        "status": "info"
    })

    # 5. Open to Work Tip
    tips.append({
        "label": "'Open to Work' Feature",
        "detail": f"Enable the 'Open to Work' feature for recruiters specifically for '{job_title}' roles in your target location.",
        "status": "pass"
    })

    return tips
