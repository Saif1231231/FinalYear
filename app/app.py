"""
MAIN APPLICATION FILE (app.py)
------------------------------
This is the heart of the CVMatchMaker website. It handles:
1. User accounts (Sign up, Login, Logout)
2. CV Uploading and processing
3. Navigating between different pages (Dashboard, Results, History)
"""

import os
import sys
import logging
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, jsonify, Response)
from flask_login import (LoginManager, login_user, logout_user,
                          login_required, current_user)

# --- CONFIGURATION SETTINGS ---

# Find the folder this file is in, so we can locate the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Create the Flask web application
app = Flask(__name__)
app.config["SECRET_KEY"] = "cvmatchmaker-secret-key"  # Used to keep user sessions secure
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'cvmatchmaker.db')}"  # Path to our database file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Turns off unnecessary tracking to save memory
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Max file upload size = 5MB

# Import our database models and connect them to the app
from models import db, User, AnalysisSession, LearningGoal
db.init_app(app)

# Set up Flask-Login to handle user sessions (who is logged in)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"  # Redirect here if not logged in

# Set up logging so we can see what's happening in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login calls this to get the current user from the database."""
    return db.session.get(User, int(user_id))

# --- PAGE ROUTES (what happens when you visit each URL) ---

@app.route("/")
def index():
    """Show the homepage (landing page with login/signup forms)."""
    return render_template("index.html")

@app.route("/dashboard")
@login_required  # Only logged-in users can access this
def dashboard():
    """Show the user's dashboard with the CV upload form and recent history."""
    # Get the last 5 analyses for this user, newest first
    history = AnalysisSession.query.filter_by(user_id=current_user.id)\
                                   .order_by(AnalysisSession.created_at.desc())\
                                   .limit(5).all()
    return render_template("dashboard.html", history=history)

@app.route("/results/<int:session_id>")
@login_required
def results(session_id):
    """Show the full results of a specific CV analysis."""
    sess = AnalysisSession.query.get_or_404(session_id)  # Find the analysis or show 404
    if sess.user_id != current_user.id:  # Make sure the user owns this analysis
        return redirect(url_for("dashboard"))
    return render_template("results.html", result=sess.get_result(), sess=sess)

@app.route("/history")
@login_required
def history():
    """Show all past analyses for this user."""
    sessions = AnalysisSession.query.filter_by(user_id=current_user.id)\
                                    .order_by(AnalysisSession.created_at.desc()).all()
    return render_template("history.html", sessions=sessions)

# --- AUTHENTICATION (Login, Signup, Logout) ---

@app.route("/login", methods=["GET"])
def login_page():
    """Show the login form (redirects to homepage with #login section)."""
    return render_template("index.html", scroll_to="login")

@app.route("/login", methods=["POST"])
def login():
    """Handle the login form submission."""
    email = request.form.get("email", "").strip().lower()  # Get email from form
    password = request.form.get("password", "")  # Get password from form
    user = User.query.filter_by(email=email).first()  # Look up user in database
    if user and user.check_password(password):  # Check if password is correct
        login_user(user)  # Log them in (creates a session cookie)
        return redirect(url_for("dashboard"))
    flash("Invalid email or password", "error")  # Show error message
    return redirect(url_for("index") + "#login")

@app.route("/signup", methods=["POST"])
def signup():
    """Handle the signup form submission."""
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if User.query.filter_by(email=email).first():  # Check if email already exists
        flash("Email already exists", "error")
        return redirect(url_for("index") + "#signup")
    new_user = User(email=email)  # Create a new user object
    new_user.set_password(password)  # Hash the password before saving
    db.session.add(new_user)  # Add to the database
    db.session.commit()  # Save changes
    login_user(new_user)  # Automatically log them in
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    """Log the user out and redirect to homepage."""
    logout_user()  # Clear the session cookie
    return redirect(url_for("index"))

# --- CV ANALYSIS (the main feature) ---

@app.route("/analyse", methods=["POST"])
@login_required
def analyse():
    """Handle CV upload, run the full AI analysis, and save results."""
    # Import the modules we need (only when needed, to keep startup fast)
    from logic.cv_parser import extract_sections, is_allowed_file
    from logic.analyser import analyse as run_analysis
    from logic.job_fetcher import fetch_jobs

    # Get the form data
    job_title = request.form.get("job_title", "").strip()
    location = request.form.get("location", "").strip()
    file = request.files.get("cv_file")

    # Validate: make sure they filled everything in
    if not job_title or not file or file.filename == "":
        flash("Missing information or no file selected", "error")
        return redirect(url_for("dashboard"))

    # Validate: make sure the file is a PDF or DOCX
    if not is_allowed_file(file.filename):
        flash("Unsupported file format. Please upload a PDF or DOCX.", "error")
        return redirect(url_for("dashboard"))

    # Step 1: Read the CV file and split it into sections
    file_bytes = file.read()
    extracted = extract_sections(file_bytes, file.filename)
    
    # Step 2: Get real job listings from Reed API
    jobs = fetch_jobs(job_title, location)
    
    # Step 3: Run the AI analysis (compare CV skills vs job skills)
    result = run_analysis(extracted["raw"], extracted["sections"], jobs, job_title, file.filename, location)

    # Step 4: Save the result to the database
    new_session = AnalysisSession(
        user_id=current_user.id,
        job_role=job_title,
        score=result["score"],
        job_count=len(jobs)
    )
    new_session.set_result(result)  # Save the full result as JSON
    db.session.add(new_session)
    db.session.commit()

    # Step 5: Redirect to the results page
    return redirect(url_for("results", session_id=new_session.id))

# --- COMPARE (side-by-side comparison of two analyses) ---

@app.route("/compare")
@login_required
def compare():
    """Let the user pick two analyses and see them side by side."""
    # Get all analyses for the dropdown menus
    sessions = AnalysisSession.query.filter_by(user_id=current_user.id)\
                                    .order_by(AnalysisSession.created_at.desc()).all()
    
    # Get the IDs from the URL (e.g. /compare?a=3&b=10)
    id_a = request.args.get("a", type=int)
    id_b = request.args.get("b", type=int)
    
    result_a = None
    result_b = None
    sess_a = None
    sess_b = None
    
    # If both IDs were provided, load both analyses
    if id_a and id_b:
        sess_a = db.session.get(AnalysisSession, id_a)
        sess_b = db.session.get(AnalysisSession, id_b)
        if sess_a and sess_a.user_id == current_user.id:  # Security check
            result_a = sess_a.get_result()
        if sess_b and sess_b.user_id == current_user.id:
            result_b = sess_b.get_result()
    
    return render_template("compare.html", sessions=sessions,
                           sess_a=sess_a, sess_b=sess_b,
                           result_a=result_a, result_b=result_b)

# --- LEARNING PATH (skill tracking to-do list) ---

@app.route("/learning-path")
@login_required
def learning_path():
    """Show the user's learning goals with progress tracking."""
    goals = LearningGoal.query.filter_by(user_id=current_user.id).all()
    total = len(goals)  # Total number of skills to learn
    done = sum(1 for g in goals if g.completed)  # How many are completed
    return render_template("learning_path.html", goals=goals, total=total, done=done)

@app.route("/add-learning-goal", methods=["POST"])
@login_required
def add_learning_goal():
    """Add a new skill to the user's learning path."""
    skill = request.form.get("skill")
    if skill:
        new_goal = LearningGoal(user_id=current_user.id, skill=skill)
        db.session.add(new_goal)
        db.session.commit()
    return redirect(url_for("learning_path"))

@app.route("/toggle-goal/<int:goal_id>", methods=["POST"])
@login_required
def toggle_learning_goal(goal_id):
    """Mark a learning goal as complete or not complete."""
    goal = db.session.get(LearningGoal, goal_id)
    if goal and goal.user_id == current_user.id:  # Security: only the owner can toggle
        goal.completed = not goal.completed  # Flip the status
        db.session.commit()
    return redirect(url_for("learning_path"))

@app.route("/delete-goal/<int:goal_id>", methods=["POST"])
@login_required
def delete_learning_goal(goal_id):
    """Remove a skill from the learning path."""
    goal = db.session.get(LearningGoal, goal_id)
    if goal and goal.user_id == current_user.id:
        db.session.delete(goal)
        db.session.commit()
    return redirect(url_for("learning_path"))

# --- JSON API (used by JavaScript on the results page) ---

@app.route("/api/learning-path/add", methods=["POST"])
@login_required
def api_add_goal():
    """API endpoint: add a skill to learning path without refreshing the page."""
    data = request.get_json()  # Read the JSON data sent by JavaScript
    skill = data.get("skill")
    if not skill:
        return jsonify({"status": "error"}), 400
    
    # Check if the skill is already in the learning path
    exists = LearningGoal.query.filter_by(user_id=current_user.id, skill=skill).first()
    if exists:
        return jsonify({"status": "exists"})  # Already added
    
    # Add the new skill
    new_goal = LearningGoal(user_id=current_user.id, skill=skill)
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"status": "added"})  # Tell JavaScript it worked

# --- EXPORTS (download reports, cover letters) ---

@app.route("/cover-letter/<int:session_id>")
@login_required
def cover_letter(session_id):
    """Show a generated cover letter based on the analysis results."""
    from logic.cover_letter_generator import generate_cover_letter
    sess = db.session.get(AnalysisSession, session_id)
    res = sess.get_result()
    # Generate the cover letter using matched and missing skills
    letter = generate_cover_letter(set(res['cv_keywords']), set(res['matched']), res['missing'], res['job_title'])
    return render_template("cover_letter.html", letter=letter, sess=sess, result=res)

@app.route("/export-cover-letter/<int:session_id>")
@login_required
def export_cover_letter(session_id):
    """Download the cover letter as a text file."""
    from logic.cover_letter_generator import generate_cover_letter
    sess = db.session.get(AnalysisSession, session_id)
    res = sess.get_result()
    letter = generate_cover_letter(set(res['cv_keywords']), set(res['matched']), res['missing'], res['job_title'])
    # Send as a downloadable text file
    return Response(letter, mimetype='text/plain', headers={"Content-Disposition": f"attachment;filename=CoverLetter_{sess.id}.txt"})

@app.route("/export-report/<int:session_id>")
@login_required
def export_report(session_id):
    """Download the analysis results as a text report."""
    sess = db.session.get(AnalysisSession, session_id)
    res = sess.get_result()
    
    # Build a simple text report
    report = f"CV MATCHMAKER REPORT\n"
    report += f"====================\n\n"
    report += f"Job Title: {res['job_title']}\n"
    report += f"Score: {res['score']}%\n"
    report += f"Grade: {res['grade']}\n\n"
    report += f"Matched Skills: {', '.join(res['matched'])}\n"
    report += f"Missing Skills: {', '.join([m['skill'] for m in res['missing']])}\n\n"
    report += f"Recommendations:\n"
    for r in res['recommendations']:
        report += f"- {r['title']}: {r['body']}\n"
    
    return Response(report, mimetype='text/plain', headers={"Content-Disposition": f"attachment;filename=CV_Report_{sess.id}.txt"})

@app.route("/delete-session/<int:session_id>", methods=["POST"])
@login_required
def delete_session(session_id):
    """Delete an analysis from the history."""
    sess = db.session.get(AnalysisSession, session_id)
    if sess and sess.user_id == current_user.id:  # Security: only owner can delete
        db.session.delete(sess)
        db.session.commit()
    return redirect(url_for("history"))

@app.route("/api/score-trend")
@login_required
def api_score_trend():
    """API: returns score history as JSON for the chart on the history page."""
    sessions = AnalysisSession.query.filter_by(user_id=current_user.id)\
                                    .order_by(AnalysisSession.created_at.asc()).all()
    # Build a list of {job_role, score, date} for JavaScript to draw the chart
    data = []
    for s in sessions:
        data.append({
            "job_role": s.job_role,
            "score": s.score,
            "date": s.created_at.strftime('%d %b %Y'),
            "date_short": s.created_at.strftime('%d/%m')
        })
    return jsonify(data)

# --- START THE SERVER ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist yet
    app.run(debug=True, port=5000)  # Start the server on port 5000
