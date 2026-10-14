from logic.cv_parser import extract_sections, is_allowed_file
from logic.skill_extractor import extract_skills_from_text


def test_allowed_file_types():
    assert is_allowed_file("cv.pdf")
    assert is_allowed_file("CV.DOCX")
    assert not is_allowed_file("cv.doc")
    assert not is_allowed_file("cv.exe")


def test_extracts_known_skills():
    skills = extract_skills_from_text("I build REST APIs with Python, Flask and PostgreSQL, deployed using Docker.")
    for expected in ("python", "flask", "docker"):
        assert expected in skills


def test_no_skills_in_unrelated_text():
    assert not extract_skills_from_text("I enjoy walking my dog in the park on Sundays.") & {"python", "java", "docker"}


def test_docx_parsing(make_docx):
    out = extract_sections(make_docx(["Skills", "Python, SQL"]).read(), "cv.docx")
    assert "Python" in out["raw"]


def test_subscores_are_computed_not_hardcoded():
    from logic.analyser import analyse
    jobs = [{"jobTitle": "Backend Developer", "jobDescription": "Python Flask Docker PostgreSQL AWS"}]
    strong = analyse("x", {"SKILLS": "Python, Flask, Docker",
                           "EXPERIENCE": "Built Flask APIs in Python and shipped them with Docker."},
                     jobs, "Backend Developer", "a.docx")
    weak = analyse("x", {"SKILLS": "Python, Flask, Docker"}, jobs, "Backend Developer", "b.docx")
    assert strong["exp_relevance_pct"] == 100
    assert weak["exp_relevance_pct"] == 0
    assert 0 <= strong["format_pct"] <= 100


def test_skill_display_names():
    from logic.skills_data import display_skill
    assert display_skill("sql") == "SQL"
    assert display_skill("node.js") == "Node.js"
    assert display_skill("c#") == "C#"
    assert display_skill("machine learning") == "Machine Learning"


def test_content_lines_are_not_treated_as_headings():
    from logic.cv_parser import _split_into_sections
    text = "EDUCATION\nBEng Software Engineering\nUniversity of Roehampton, London\nWORK EXPERIENCE\nSales Associate | 2023"
    sections = _split_into_sections(text)
    assert "University of Roehampton, London" in sections["EDUCATION"]
    assert "Sales Associate" in sections["EXPERIENCE"]


def test_sample_jobs_match_the_search_and_are_labelled():
    from logic.job_fetcher import fetch_jobs, SOURCE_SAMPLE
    jobs, source = fetch_jobs("Junior Backend Developer")
    assert source == SOURCE_SAMPLE
    assert len(jobs) >= 5
    assert "Backend" in jobs[0]["jobTitle"]
    assert all("jobUrl" not in j for j in jobs)  # no fake links to Reed
