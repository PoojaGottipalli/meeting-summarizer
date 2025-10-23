import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv

# --- Define paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                    # meeting-summarizer/
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")       # frontend/

# --- Add project root to sys.path ---
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --- Load environment variables (.env inside backend) ---
load_dotenv(os.path.join(BASE_DIR, ".env"))

# --- Import Blueprints ---
from routes.meeting import meetings_bp
from routes.sessions import sessions_bp

# --- Create Flask app ---
app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),  # ✅ correct path
    static_folder=os.path.join(FRONTEND_DIR, "static")        # ✅ correct path
)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET", "dev-secret")

# --- Register blueprints ---
app.register_blueprint(meetings_bp)
app.register_blueprint(sessions_bp)

# --- Frontend routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/meetings")
def meetings_page():
    return render_template("mettings.html")  # ✅ matches your file name

# --- Run app ---
if __name__ == "__main__":
    print("✅ Template path:", os.path.join(FRONTEND_DIR, "templates"))
    app.run(debug=True, host="0.0.0.0", port=5000)
