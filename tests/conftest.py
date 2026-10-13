import io
import os
import sys

import pytest

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
sys.path.insert(0, os.path.abspath(APP_DIR))

# Use an in-memory database and no external job API during tests
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.pop("REED_API_KEY", None)

from app import app as flask_app  # noqa: E402
from models import db  # noqa: E402


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True, SECRET_KEY="test")
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


def signup(client, email="user@example.com", password="password123"):
    return client.post("/signup", data={"email": email, "password": password})


@pytest.fixture
def make_docx():
    """Build a small .docx CV in memory."""
    def _make(lines):
        from docx import Document
        doc = Document()
        for line in lines:
            doc.add_paragraph(line)
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf
    return _make
