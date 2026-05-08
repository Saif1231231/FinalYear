"""
DATABASE MODELS (models.py)
--------------------------
This file defines how our data is stored in the database.
We use SQLAlchemy, which lets us treat database tables like Python classes.
"""

import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database object
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    USER TABLE: Stores information about people who sign up.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: one user → many sessions
    sessions = db.relationship("AnalysisSession", backref="user", lazy=True,
                                cascade="all, delete-orphan")

    def set_password(self, password):
        """Turn a plain-text password into a secure hash."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class AnalysisSession(db.Model):
    """
    ANALYSIS TABLE: Stores the summary of each CV analysis.
    We save the full matching data as a JSON string.
    """
    __tablename__ = "analysis_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    job_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # This stores the complex analysis results (skills, recs, etc.) as text
    result_json = db.Column(db.Text, nullable=True)

    def set_result(self, data_dict):
        """Convert a Python dictionary to a JSON string for saving."""
        self.result_json = json.dumps(data_dict, default=str)

    def get_result(self):
        """Convert the saved JSON string back into a Python dictionary."""
        if not self.result_json:
            return {}
        try:
            return json.loads(self.result_json)
        except (json.JSONDecodeError, TypeError):
            return {}

    def matched_list(self):
        """Helper for template compatibility."""
        return self.get_result().get("matched", [])

    def missing_list(self):
        """Helper for template compatibility."""
        return self.get_result().get("missing", [])

    def __repr__(self):
        return f"<AnalysisSession job={self.job_role} score={self.score}>"


class LearningGoal(db.Model):
    """
    Tracks a skill the user wants to learn (from their missing skills).
    Users can mark goals as completed to track their progress.
    """
    __tablename__ = "learning_goals"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill       = db.Column(db.String(100), nullable=False)
    job_role    = db.Column(db.String(200), default="")   # which analysis it came from
    completed   = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", backref=db.backref("learning_goals", lazy=True))

    def __repr__(self):
        return f"<LearningGoal {self.skill} done={self.completed}>"
