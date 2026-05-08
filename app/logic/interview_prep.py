# interview_prep.py
# Feature: AI-Powered Interview Prep
#
# Generates a list of tailored interview questions based on the target job
# role and the specific skills identified as "missing" from the user's CV.

def generate_interview_questions(job_title, missing_skills):
    """
    Returns a list of 5 tailored interview questions.
    """
    questions = []

    # 1. Behavioral Question (Role specific)
    questions.append({
        "question": f"Can you describe a challenging project where you acted as a {job_title} and how you handled it?",
        "tip": "Focus on the 'STAR' method (Situation, Task, Action, Result) and highlight your problem-solving skills."
    })

    # 2. Technical Questions (Based on missing skills)
    if missing_skills:
        top_missing = missing_skills[0]['skill'].title()
        questions.append({
            "question": f"How would you approach a project that requires deep knowledge of {top_missing}?",
            "tip": f"Be honest about your current level. Mention that you are proactively learning {top_missing} (as seen in your Learning Path!) and explain your methodology for picking up new tech."
        })

        if len(missing_skills) > 1:
            second_missing = missing_skills[1]['skill'].title()
            questions.append({
                "question": f"What are the key benefits of using {second_missing} over competing technologies in a production environment?",
                "tip": "Explain the architectural advantages and why an organisation would choose it for scalability or performance."
            })

    # 3. Standard but important questions
    questions.append({
        "question": "Where do you see yourself in five years within this industry?",
        "tip": "Show ambition but keep it grounded in the role you are applying for. Mention specific skills you want to master."
    })

    questions.append({
        "question": f"Why do you want to work as a {job_title} for our company specifically?",
        "tip": "Research the company's recent news or mission statement and link it back to your own career goals."
    })

    return questions[:5]
