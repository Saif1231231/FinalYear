"""
JOB FETCHER (job_fetcher.py)
---------------------------
Gets real job listings from the Reed.co.uk API.

Without a REED_API_KEY (or if Reed is down) it falls back to a built-in set of
sample listings so the site still works. Results always say where they came
from, so the page never presents sample data as real jobs.
"""

import os
import logging
import requests
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

REED_API_BASE = "https://www.reed.co.uk/api/1.0"
REED_API_KEY = os.environ.get("REED_API_KEY", "")

SOURCE_REED = "reed"
SOURCE_SAMPLE = "sample"

# --- SAMPLE DATA ---
# Representative UK tech listings (fictional employers) used in demo mode.
# Descriptions reflect the kind of requirements real adverts ask for, so the
# skill gap analysis still produces a useful result.

SAMPLE_JOBS = [
    {"jobTitle": "Graduate Software Engineer", "employerName": "Northbank Digital", "locationName": "London",
     "minimumSalary": 32000, "maximumSalary": 38000,
     "jobDescription": "Join our product team building web applications in Python and JavaScript. You'll write REST APIs, work with PostgreSQL, use Git and code review, and learn Docker and AWS. Agile team, unit testing expected."},
    {"jobTitle": "Junior Software Engineer", "employerName": "Halden Systems", "locationName": "London",
     "minimumSalary": 35000, "maximumSalary": 42000,
     "jobDescription": "Junior engineer to work on our TypeScript and React front end and Node.js services. Experience with SQL, Git, CI/CD and testing (Jest) is a plus. Scrum team."},
    {"jobTitle": "Software Engineer", "employerName": "Kestrel Payments", "locationName": "London",
     "minimumSalary": 50000, "maximumSalary": 65000,
     "jobDescription": "Build and run payment services in Java and Spring Boot on AWS. Microservices, Kafka, PostgreSQL, Docker and Kubernetes. Strong testing culture with CI/CD."},
    {"jobTitle": "Software Engineer", "employerName": "Bramble Health", "locationName": "Manchester",
     "minimumSalary": 45000, "maximumSalary": 58000,
     "jobDescription": "Python and Django engineer for our patient platform. REST APIs, PostgreSQL, Redis, Docker, GitHub Actions. Some React on the front end. Agile."},
    {"jobTitle": "Junior Backend Developer", "employerName": "Ledgerline", "locationName": "London",
     "minimumSalary": 33000, "maximumSalary": 40000,
     "jobDescription": "Backend developer using Python, Flask or FastAPI, and PostgreSQL. You'll design REST APIs, write SQL, use Docker and Git, and deploy to Azure. Unit testing with pytest."},
    {"jobTitle": "Backend Developer", "employerName": "Orbit Logistics", "locationName": "Birmingham",
     "minimumSalary": 45000, "maximumSalary": 55000,
     "jobDescription": "Node.js and Express backend developer. MongoDB and PostgreSQL, REST and GraphQL APIs, Docker, AWS Lambda, CI/CD. TypeScript preferred."},
    {"jobTitle": "Full Stack Developer", "employerName": "Fernway Studio", "locationName": "London",
     "minimumSalary": 40000, "maximumSalary": 52000,
     "jobDescription": "Full stack developer with React, Next.js, TypeScript and Node.js. PostgreSQL, Prisma, Tailwind, Git. Deploying on Vercel and AWS. Agile."},
    {"jobTitle": "Graduate Full Stack Developer", "employerName": "Copperleaf", "locationName": "Leeds",
     "minimumSalary": 28000, "maximumSalary": 34000,
     "jobDescription": "Graduate role across our C# and .NET backend and React front end. SQL Server, Azure DevOps, Git, unit testing. Training provided."},
    {"jobTitle": "Frontend Developer", "employerName": "Pixel & Pine", "locationName": "Bristol",
     "minimumSalary": 38000, "maximumSalary": 48000,
     "jobDescription": "Frontend developer with React, TypeScript, HTML, CSS and accessibility knowledge. Jest, Git, Figma, REST APIs."},
    {"jobTitle": "Data Engineer", "employerName": "Rivermark Analytics", "locationName": "London",
     "minimumSalary": 50000, "maximumSalary": 65000,
     "jobDescription": "Build data pipelines in Python and SQL with Apache Spark, Airflow and Azure Databricks. Docker, Git, CI/CD. Experience with PostgreSQL and cloud (AWS or Azure)."},
    {"jobTitle": "Data Analyst", "employerName": "Greywell Retail", "locationName": "Manchester",
     "minimumSalary": 32000, "maximumSalary": 40000,
     "jobDescription": "Data analyst using SQL, Python (pandas) and Excel to build dashboards in Power BI or Tableau. Stakeholder communication skills."},
    {"jobTitle": "DevOps Engineer", "employerName": "Stackhaven", "locationName": "London",
     "minimumSalary": 55000, "maximumSalary": 70000,
     "jobDescription": "DevOps engineer working with AWS, Terraform, Kubernetes, Docker, Linux, Bash and GitHub Actions. Monitoring with Prometheus and Grafana. Python scripting."},
    {"jobTitle": "Machine Learning Engineer", "employerName": "Lumen Labs", "locationName": "Cambridge",
     "minimumSalary": 55000, "maximumSalary": 75000,
     "jobDescription": "ML engineer with Python, PyTorch, scikit-learn, NLP, Docker and AWS. Experience deploying models behind REST APIs and working with SQL."},
    {"jobTitle": "Junior Python Developer", "employerName": "Tidewater Tech", "locationName": "Remote",
     "minimumSalary": 30000, "maximumSalary": 37000,
     "jobDescription": "Python developer to build internal tools with Flask and Django. SQL, PostgreSQL, Git, Linux, Docker. NLP experience with spaCy is a bonus."},
]

# Words that describe seniority rather than the job itself, ignored when matching titles.
_TITLE_NOISE = {"junior", "graduate", "senior", "lead", "entry", "level", "trainee", "intern", "the", "a", "and"}


def _title_words(title: str) -> set:
    return {w for w in title.lower().replace("-", " ").split() if w not in _TITLE_NOISE}


def _sample_jobs_for(job_title: str) -> List[Dict]:
    """Pick sample listings whose titles share words with the search, e.g.
    'Junior Backend Developer' matches 'Backend Developer' listings."""
    wanted = _title_words(job_title)
    scored = []
    for job in SAMPLE_JOBS:
        overlap = len(wanted & _title_words(job["jobTitle"]))
        if overlap:
            scored.append((overlap, job))
    scored.sort(key=lambda pair: -pair[0])

    # Take the closest titles first, then the next-closest only until we have 5.
    # Otherwise "Software Engineer" would also pull in every "... Engineer" role.
    matches = []
    for overlap, job in scored:
        if matches and overlap < scored[0][0] and len(matches) >= 5:
            break
        matches.append(job)

    # Never compare against an empty or tiny market: top up with general software roles.
    if len(matches) < 5:
        matches += [j for j in SAMPLE_JOBS if j not in matches and "software" in j["jobTitle"].lower()]
    return matches[:8]


def _get_from_reed_api(job_title, location=""):
    """Download live listings from Reed (up to 15)."""
    params = {"keywords": job_title, "resultsToTake": 15}
    if location:
        params["locationName"] = location
    try:
        response = requests.get(f"{REED_API_BASE}/search", params=params, auth=(REED_API_KEY, ""), timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        logger.error("Reed API error: %s", e)
        return []


def fetch_jobs(job_title, location="") -> Tuple[List[Dict], str]:
    """Return (jobs, source). Tries Reed first, then falls back to sample listings."""
    if REED_API_KEY:
        jobs = _get_from_reed_api(job_title, location)
        if jobs:
            return jobs, SOURCE_REED
        logger.warning("Reed returned nothing, using sample listings")
    else:
        logger.info("No REED_API_KEY set, using sample listings")
    return _sample_jobs_for(job_title), SOURCE_SAMPLE
