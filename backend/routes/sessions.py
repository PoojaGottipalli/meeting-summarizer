from flask import Blueprint, request, jsonify
import sqlite3
from backend.db import init_db, DB_PATH


sessions_bp = Blueprint("sessions_bp", __name__, url_prefix="/api/v1/sessions")

@sessions_bp.route("/", methods=["GET"])
def list_sessions():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, context, created_at FROM sessions ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    sessions = [{"id": r[0], "context": r[1], "created_at": r[2]} for r in rows]
    return jsonify(sessions)
