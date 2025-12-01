import os
import sqlite3
from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from backend.db import init_db, DB_PATH

from backend.llm import transcribe_with_gemini, summarize_meeting_with_tags


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
        return redirect(url_for("home"))

    file = request.files["audio"]
    if file.filename == "":
        return redirect(url_for("home"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        try:
            transcript = transcribe_with_gemini(save_path)
        except Exception as e:
            print(f"Transcription failed: {e}")
            return redirect(url_for("home"))

        try:
            summary, people, action_items = summarize_meeting_with_tags(transcript)
        except Exception as e:
            print(f"Summarization failed: {e}")
            summary, people, action_items = ("", "", "")

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
            
            return redirect(url_for("meetings_bp.view_meeting", meeting_id=meeting_id))
        except Exception as e:
            print(f"Database save failed: {e}")
            return redirect(url_for("home"))

    else:
        return redirect(url_for("home"))


@meetings_bp.route("/meetings/list", methods=["GET"])
def list_meetings():
    """Fetch all meetings as JSON for the meetings list page."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, filename, summary, created_at FROM meetings ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()

    meetings = [
        {
            "id": row[0],
            "filename": row[1],
            "summary": row[2][:100] + "..." if row[2] and len(row[2]) > 100 else row[2],
            "created_at": row[3],
        }
        for row in rows
    ]
    
    from flask import jsonify
    return jsonify(meetings)


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
