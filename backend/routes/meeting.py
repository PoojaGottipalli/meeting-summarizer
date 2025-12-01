import os
import sqlite3
from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from backend.db import init_db, DB_PATH

from llm import transcribe_with_gemini, summarize_meeting_with_tags

meetings_bp = Blueprint("meetings_bp", __name__, url_prefix="/api/v1")

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "flac", "ogg"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@meetings_bp.route("/upload", methods=["POST"])
def upload():
    """Handle audio upload, transcription, and summarization."""
    if "audio" not in request.files:
        flash("No file part in request")
        return redirect(url_for("home"))

    file = request.files["audio"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("home"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Step 1: Transcribe audio
        try:
            transcript = transcribe_with_gemini(save_path)
        except Exception as e:
            flash(f"Transcription failed: {e}")
            return redirect(url_for("home"))

        # Step 2: Summarize and extract action items
        try:
            summary, people, action_items = summarize_meeting_with_tags(transcript)
        except Exception as e:
            flash(f"Summarization failed: {e}")
            summary, people, action_items = ("", "", "")

        # Step 3: Save to SQLite
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO meetings (filename, attendees, transcript, summary, people, action_items, created_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            """, (filename, "", transcript, summary, people, action_items))
            meeting_id = cur.lastrowid
            conn.commit()
            conn.close()
        except Exception as e:
            flash(f"Database save failed: {e}")
            return redirect(url_for("home"))

        return redirect(url_for("meetings_bp.view_meeting", meeting_id=meeting_id))

    else:
        flash("Unsupported file type. Please upload a valid audio file.")
        return redirect(url_for("home"))


@meetings_bp.route("/meetings/<int:meeting_id>")
def view_meeting(meeting_id):
    """Display meeting details."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, filename, transcript, summary, action_items, created_at FROM meetings WHERE id = ?",
        (meeting_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        flash("Meeting not found")
        return redirect(url_for("home"))

    meeting = {
        "id": row[0],
        "filename": row[1],
        "transcript": row[2],
        "summary": row[3],
        "action_items": row[4],
        "created_at": row[5],
    }

    return render_template("meetings.html", meeting=meeting)
