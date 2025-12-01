import os
from dotenv import load_dotenv

# Import the GenAI client lazily below so the Flask app can start even when
# the `google`/`genai` package is not installed during development.
genai = None

# Load local environment variables from `.env` when present
load_dotenv()

# Read API key from environment (Railway or local .env)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini client lazily. Avoid raising on import so the web app can
# start even when the API key isn't configured. Functions below will raise
# a clear error if the client isn't available when called.
client = None
if GEMINI_API_KEY:
    try:
        # Try lazy import of the GenAI client
        from google import genai as _genai
        genai = _genai
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        # Missing package or client init failed — keep client as None so we
        # raise a helpful error only when a function actually needs the LLM.
        client = None
        genai = None

def _ensure_client():
    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY not configured. Set the environment variable 'GEMINI_API_KEY'"
        )

def transcribe_with_gemini(filepath):
    _ensure_client()
    uploaded = client.files.upload(file=filepath)
    prompt = "Generate a full transcript of this meeting audio file."
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, uploaded],
    )
    return getattr(resp, "text", str(resp))

def summarize_meeting_with_tags(text):
    prompt = (
        "Summarize this meeting transcript into:\n"
        "SUMMARY: key discussion points (5-6 bullet points)\n"
        "ACTION_ITEMS: tasks or follow-ups.\n"
        "Return plain text with these sections clearly marked."
    )
    _ensure_client()
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, text],
    )
    out = getattr(resp, "text", str(resp))

    summary = extract_section(out, "SUMMARY:") or ""
    action_items = extract_section(out, "ACTION_ITEMS:") or ""

    return summary.strip(), "", action_items.strip()

def extract_section(blob, header):
    idx = blob.find(header)
    if idx == -1:
        return None

    rest = blob[idx + len(header):]
    for h in ["SUMMARY:", "ACTION_ITEMS:"]:
        if h != header and h in rest:
            rest = rest[:rest.find(h)]

    return rest.strip()