# cover_letter_generator.py
# Feature: Auto-generated Cover Letter
#
# Generates a professional cover letter draft based on the user's CV skills,
# the target job title, and the key requirements found in job listings.

def generate_cover_letter(cv_skills, matched_skills, missing_skills, job_title, employer_name="Hiring Manager", location=""):
    """
    Generates a cover letter draft.
    """
    import random

    # Action verbs for variety
    openers = [
        f"I am writing to express my strong interest in the {job_title} position.",
        f"I was excited to see the opening for a {job_title} role and believe my skills align perfectly with your requirements.",
        f"Please accept this letter as a formal application for the {job_title} position."
    ]

    # Matched skills section
    skills_list = [s.title() for s in list(matched_skills)[:4]]
    if not skills_list:
        skills_list = [s.title() for s in list(cv_skills)[:4]]

    skills_sentence = ""
    if skills_list:
        skills_sentence = f"With a solid foundation in {', '.join(skills_list[:-1])} and {skills_list[-1]}, I have successfully delivered projects that meet high industry standards."

    # Experience paragraph
    experience_para = (
        f"Throughout my career, I have focused on building robust and scalable solutions. "
        f"My experience in {job_title} roles has allowed me to develop a keen eye for detail and a commitment to continuous improvement. "
        f"{skills_sentence}"
    )

    # Closing
    closings = [
        "I am eager to bring my unique perspective and technical expertise to your team.",
        "I am confident that my background makes me an ideal candidate for this role.",
        "I look forward to the possibility of discussing how my skills can contribute to your company's success."
    ]

    letter = [
        "Dear " + employer_name + ",",
        "",
        random.choice(openers),
        "",
        experience_para,
        "",
        "I am particularly drawn to this opportunity because of the innovative work being done in the field. I am a fast learner and am already working on expanding my skillset, including learning " + (missing_skills[0]['skill'].title() if missing_skills else "new industry-standard tools") + ", to ensure I can hit the ground running.",
        "",
        random.choice(closings),
        "",
        "Sincerely,",
        "[Your Name]"
    ]

    return "\n".join(letter)
