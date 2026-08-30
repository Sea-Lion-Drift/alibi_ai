from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import random

# Import webcam stream
from AI.webcam import generate_frames

app = Flask(__name__)

# Store candidate details temporarily
candidate_data = {}
# ==========================================
# LIVE INTERVIEW STATS
# ==========================================

from AI.stats import interview_stats
# ==========================
# INTERVIEW QUESTIONS
# ==========================

questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "Describe a difficult situation you handled.",
    "Where do you see yourself in five years?"
]


# ===================================================
# HOME
# ===================================================
@app.route('/')
def home():
    return render_template("index.html")


# ===================================================
# LOGIN
# ===================================================
@app.route('/login')
def login():
    return render_template("login.html")


# ===================================================
# DASHBOARD
# ===================================================
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# ===================================================
# NEW INTERVIEW
# ===================================================
@app.route('/new_interview', methods=["GET", "POST"])
def new_interview():

    if request.method == "POST":

        candidate_data.clear()
        # Reset AI Statistics
        interview_stats["total_frames"] = 0
        interview_stats["eye_contact_frames"] = 0
        interview_stats["phone_detected"] = False
        interview_stats["multiple_faces"] = False
        interview_stats["looking_away_frames"] = 0
        interview_stats["emotion"] = "Neutral"
        interview_stats["head_movement"] = "Normal"
        interview_stats["voice_confidence"] = 95
        interview_stats["looking_away_frames"]

        candidate_data["name"] = request.form.get("name")
        candidate_data["email"] = request.form.get("email")
        candidate_data["phone"] = request.form.get("phone")
        candidate_data["position"] = request.form.get("position")
        candidate_data["experience"] = request.form.get("experience")
        candidate_data["department"] = request.form.get("department")
        candidate_data["interview_type"] = request.form.get("interview_type")
        candidate_data["mode"] = request.form.get("mode")
        candidate_data["notes"] = request.form.get("notes")

        candidate_data["interview_id"] = (
            "INT-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + str(random.randint(100, 999))
        )

        candidate_data["date"] = datetime.now().strftime("%d %B %Y")
        candidate_data["time"] = datetime.now().strftime("%I:%M %p")

        return redirect(url_for("success"))

    return render_template("new_interview.html")


# ===================================================
# SUCCESS PAGE
# ===================================================
@app.route('/success')
def success():

    if not candidate_data:
        return redirect(url_for("new_interview"))

    return render_template(
        "success.html",
        candidate=candidate_data
    )


# ===================================================
# INTERVIEW PAGE
# ===================================================
# ==========================
# INTERVIEW PAGE
# ==========================

@app.route("/interview")
def interview():

    if not candidate_data:
        return redirect(url_for("new_interview"))

    return render_template(
        "interview.html",
        candidate=candidate_data,
        questions=questions
    )

# ===================================================
# LIVE CAMERA FEED
# ===================================================
@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# ===================================================
# ===================================================
# AI REPORT
# ===================================================

@app.route('/report')
def report():

    if not candidate_data:
        return redirect(url_for("dashboard"))

    # -------------------------------
    # Eye Contact Percentage
    # -------------------------------

    if interview_stats["total_frames"] > 0:

        eye_contact = int(
            interview_stats["eye_contact_frames"]
            /
            interview_stats["total_frames"]
            * 100
        )

    else:

        eye_contact = 100

    # -------------------------------
    # Fraud Score Calculation
    # -------------------------------

    cheating_probability = 0

    # Phone Detection
    if interview_stats["phone_detected"]:
        cheating_probability += 40

    # Multiple Person
    if interview_stats["multiple_faces"]:
        cheating_probability += 30

    # Eye Contact
    if eye_contact < 70:
        cheating_probability += 20

    # Looking Away
    if interview_stats["looking_away_frames"] > 150:
        cheating_probability += 10

    cheating_probability = min(cheating_probability, 100)

    # -------------------------------
    # Risk Level
    # -------------------------------

    if cheating_probability <= 25:

        risk = "LOW RISK"
        color = "#22c55e"

    elif cheating_probability <= 60:

        risk = "MEDIUM RISK"
        color = "#f59e0b"

    else:

        risk = "HIGH RISK"
        color = "#ef4444"

    # -------------------------------
    # Report Data
    # -------------------------------

    report_data = {

        "face_detected": "Yes",

        "multiple_faces":
            "Yes" if interview_stats["multiple_faces"] else "No",

        "eye_contact": eye_contact,

        "emotion":
            interview_stats["emotion"],

        "head_movement":
            interview_stats["head_movement"],

        "voice_confidence":
            interview_stats["voice_confidence"],

        "tab_switches":
            interview_stats["tab_switches"],

        "phone_detected":
            "Yes" if interview_stats["phone_detected"] else "No",

        "cheating_probability":
            cheating_probability,

        "risk":
            risk,

        "color":
            color

    }

    return render_template(
        "report.html",
        candidate=candidate_data,
        report=report_data
    )

# ===================================================
# RUN APP
# ===================================================
if __name__ == "__main__":
    app.run(debug=True)