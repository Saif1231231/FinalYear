# job_title_suggester.py
# Feature: Alternative Job Title Suggestions
#
# Compares the user's CV skills against a curated map of common job titles
# and their typical required skills.  Returns the top alternative roles
# ranked by match percentage so the user can discover roles they may not
# have considered.

import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Job title → typical skills mapping
# Curated from common UK job listings (Reed, Indeed, LinkedIn)
# ─────────────────────────────────────────────────────────────────────────────

JOB_SKILL_MAP: Dict[str, Set[str]] = {
    "Software Engineer": {
        "python", "javascript", "java", "sql", "git", "docker",
        "aws", "react", "node.js", "ci/cd", "agile", "typescript",
        "rest", "linux", "kubernetes", "testing",
    },
    "Frontend Developer": {
        "javascript", "react", "html", "css", "typescript", "git",
        "responsive design", "figma", "sass", "webpack", "node.js",
        "vue", "angular", "testing", "agile",
    },
    "Backend Developer": {
        "python", "java", "sql", "postgresql", "mongodb", "docker",
        "aws", "rest", "node.js", "git", "linux", "redis",
        "ci/cd", "kubernetes", "microservices",
    },
    "Full Stack Developer": {
        "javascript", "python", "react", "node.js", "sql", "html",
        "css", "git", "docker", "mongodb", "aws", "typescript",
        "rest", "agile", "testing",
    },
    "Data Analyst": {
        "python", "sql", "excel", "tableau", "power bi", "pandas",
        "statistics", "data visualisation", "r", "communication",
        "reporting", "analytical", "numpy", "jupyter",
    },
    "Data Scientist": {
        "python", "machine learning", "sql", "pandas", "numpy",
        "scikit-learn", "tensorflow", "statistics", "r",
        "data visualisation", "jupyter", "deep learning", "nlp",
    },
    "Data Engineer": {
        "python", "sql", "spark", "aws", "docker", "postgresql",
        "etl", "kafka", "airflow", "data pipelines", "pandas",
        "linux", "git", "cloud", "big data",
    },
    "DevOps Engineer": {
        "docker", "kubernetes", "aws", "linux", "ci/cd", "terraform",
        "ansible", "git", "python", "jenkins", "monitoring",
        "bash", "networking", "cloud", "scripting",
    },
    "Cloud Engineer": {
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "linux", "networking", "ci/cd", "python", "security",
        "cloud", "infrastructure", "monitoring",
    },
    "Machine Learning Engineer": {
        "python", "machine learning", "tensorflow", "pytorch",
        "scikit-learn", "deep learning", "nlp", "docker", "aws",
        "sql", "pandas", "numpy", "git", "mlops",
    },
    "QA Engineer": {
        "testing", "selenium", "python", "java", "git", "agile",
        "jira", "sql", "automation", "ci/cd", "api testing",
        "communication", "analytical", "quality assurance",
    },
    "Cyber Security Analyst": {
        "security", "networking", "linux", "python", "firewalls",
        "siem", "penetration testing", "incident response",
        "risk assessment", "encryption", "compliance", "monitoring",
    },
    "Project Manager (IT)": {
        "agile", "scrum", "jira", "communication", "leadership",
        "project management", "stakeholder management", "risk management",
        "budgeting", "reporting", "microsoft project", "analytical",
    },
    "Business Analyst": {
        "sql", "excel", "communication", "analytical", "stakeholder management",
        "requirements gathering", "jira", "reporting", "data visualisation",
        "agile", "project management", "power bi", "uml",
    },
    "UX/UI Designer": {
        "figma", "sketch", "adobe xd", "html", "css", "user research",
        "wireframing", "prototyping", "responsive design", "accessibility",
        "design thinking", "communication", "typography",
    },
    "Systems Administrator": {
        "linux", "windows server", "networking", "bash", "python",
        "active directory", "dns", "monitoring", "security",
        "virtualisation", "docker", "cloud", "scripting",
    },
    "Mobile Developer": {
        "swift", "kotlin", "react native", "flutter", "java",
        "javascript", "git", "rest", "firebase", "agile",
        "testing", "ci/cd", "ui design",
    },
    "Database Administrator": {
        "sql", "postgresql", "mysql", "mongodb", "oracle",
        "database design", "performance tuning", "backup",
        "linux", "scripting", "security", "cloud", "python",
    },
}


def suggest_alternative_titles(
    cv_skills: Set[str],
    current_title: str = "",
    top_n: int = 5,
) -> List[Dict]:
    """
    Compare the user's CV skills against known job title profiles.
    Returns up to `top_n` alternative job titles ranked by match %.

    Each returned dict:
        {
            "title": "Data Analyst",
            "match_pct": 72,
            "matched_skills": ["python", "sql", ...],
            "skills_needed": ["tableau", ...],
            "is_current": False,
        }
    """
    # Normalise CV skills to lowercase
    cv_lower = {s.lower().strip() for s in cv_skills if s}

    results = []

    for title, required_skills in JOB_SKILL_MAP.items():
        matched = cv_lower & required_skills
        missing = required_skills - cv_lower
        match_pct = round((len(matched) / len(required_skills)) * 100) if required_skills else 0

        results.append({
            "title": title,
            "match_pct": match_pct,
            "matched_skills": sorted(matched),
            "skills_needed": sorted(missing),
            "is_current": title.lower().strip() == current_title.lower().strip(),
        })

    # Sort by match % descending
    results.sort(key=lambda x: x["match_pct"], reverse=True)

    # Always include the current title if it exists in results, then fill up to top_n
    current = [r for r in results if r["is_current"]]
    others  = [r for r in results if not r["is_current"]]

    # Return current title (if found) + top alternatives
    final = current + others
    return final[:top_n]
