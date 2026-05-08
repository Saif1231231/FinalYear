"""
JOB FETCHER (job_fetcher.py)
---------------------------
This file gets real job listings from the Reed.co.uk API.
If you don't have an API key, it uses 'Mock Data' (fake jobs) 
so you can still test the website.
"""

import os
import logging
import requests
from typing import List, Dict

logger = logging.getLogger(__name__)

# The website we get jobs from
REED_API_BASE = "https://www.reed.co.uk/api/1.0"
# Look for the API key in your computer's settings
REED_API_KEY  = os.environ.get("REED_API_KEY", "")

# --- MOCK DATA (Fake jobs used for testing) ---

MOCK_JOBS = [
    {
        "jobId": 1,
        "jobTitle": "Software Engineer",
        "employerName": "Tech Solutions Ltd",
        "locationName": "London",
        "minimumSalary": 55000,
        "maximumSalary": 75000,
        "jobDescription": "We need a Software Engineer who knows Python, React, and SQL. You will work on cloud projects using AWS and Docker.",
        "jobUrl": "https://www.reed.co.uk/jobs/software-engineer/1"
    },
    {
        "jobId": 2,
        "jobTitle": "Data Analyst",
        "employerName": "DataCorp",
        "locationName": "Manchester",
        "minimumSalary": 35000,
        "maximumSalary": 45000,
        "jobDescription": "Seeking a Data Analyst to work with SQL, Python, and Excel. You will build dashboards using Tableau or Power BI.",
        "jobUrl": "https://www.reed.co.uk/jobs/data-analyst/2"
    }
]

def _get_from_reed_api(job_title, location=""):
    """Connect to the Reed website and download real job data."""
    params = {"keywords": job_title, "resultsToTake": 15}
    if location:
        params["locationName"] = location

    try:
        # We send the API key for permission to read their data
        response = requests.get(
            f"{REED_API_BASE}/search",
            params=params,
            auth=(REED_API_KEY, ""),
            timeout=10
        )
        response.raise_for_status() # Check for errors
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        logger.error("API Error: %s", e)
        return []

def fetch_jobs(job_title, location=""):
    """
    The main function to get jobs. 
    It tries the real API first, then falls back to fake data if needed.
    """
    if REED_API_KEY:
        jobs = _get_from_reed_api(job_title, location)
        if jobs:
            return jobs

    # If API failed or no key was provided, use our fake list
    logger.info("Using mock data because no API key was found.")
    
    # Filter fake data to match the search
    keyword = job_title.lower()
    relevant = [j for j in MOCK_JOBS if keyword in j["jobTitle"].lower()]
    
    return relevant if relevant else MOCK_JOBS
