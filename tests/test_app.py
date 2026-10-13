from conftest import signup

CV_LINES = [
    "Jane Doe",
    "jane@example.com | 07123 456789 | linkedin.com/in/janedoe",
    "Profile",
    "Backend developer experienced in Python, Flask and PostgreSQL.",
    "Skills",
    "Python, Flask, SQL, PostgreSQL, Docker, Git, REST APIs",
    "Experience",
    "Built REST APIs in Flask backed by PostgreSQL and deployed them with Docker.",
    "Education",
    "BEng Software Engineering",
]


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_homepage_loads(client):
    assert client.get("/").status_code == 200


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_signup_then_login(client):
    assert signup(client).status_code == 302
    client.get("/logout")
    resp = client.post("/login", data={"email": "user@example.com", "password": "password123"})
    assert resp.headers["Location"].endswith("/dashboard")


def test_signup_rejects_short_password(client):
    signup(client, password="short")
    assert client.get("/dashboard").status_code == 302  # not logged in


def test_duplicate_email_rejected(client):
    signup(client)
    client.get("/logout")
    signup(client, password="anotherpass")
    assert client.get("/dashboard").status_code == 302


def test_wrong_password(client):
    signup(client)
    client.get("/logout")
    client.post("/login", data={"email": "user@example.com", "password": "wrongpass1"})
    assert client.get("/dashboard").status_code == 302


def test_rejects_unsupported_file(client):
    signup(client)
    resp = client.post("/analyse", data={
        "job_title": "Backend Developer",
        "cv_file": (__import__("io").BytesIO(b"hello"), "cv.txt"),
    }, content_type="multipart/form-data")
    assert resp.headers["Location"].endswith("/dashboard")


def _analyse(client, make_docx):
    return client.post("/analyse", data={
        "job_title": "Backend Developer",
        "location": "London",
        "cv_file": (make_docx(CV_LINES), "cv.docx"),
    }, content_type="multipart/form-data")


def test_full_analysis_flow(client, make_docx):
    signup(client)
    resp = _analyse(client, make_docx)
    assert resp.status_code == 302 and "/results/" in resp.headers["Location"]
    page = client.get(resp.headers["Location"])
    assert page.status_code == 200
    trend = client.get("/api/score-trend").get_json()
    assert len(trend) == 1 and 0 <= trend[0]["score"] <= 100


def test_users_cannot_see_each_others_results(client, make_docx):
    signup(client, email="alice@example.com")
    url = _analyse(client, make_docx).headers["Location"]
    session_id = url.rstrip("/").split("/")[-1]
    client.get("/logout")

    signup(client, email="bob@example.com")
    for path in (f"/results/{session_id}", f"/cover-letter/{session_id}",
                 f"/export-report/{session_id}", f"/export-cover-letter/{session_id}"):
        assert client.get(path).status_code == 404, path


def test_learning_path_api(client):
    signup(client)
    assert client.post("/api/learning-path/add", json={"skill": "docker"}).get_json()["status"] == "added"
    assert client.post("/api/learning-path/add", json={"skill": "docker"}).get_json()["status"] == "exists"
    assert client.post("/api/learning-path/add", json={}).status_code == 400
