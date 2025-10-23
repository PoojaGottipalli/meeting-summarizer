import os
from google import genai

# Initialize Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

def transcribe_with_gemini(filepath):
    uploaded = client.files.upload(file=filepath)
    prompt = "Generate a full transcript of this meeting audio file."
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, uploaded])
    return getattr(resp, "text", str(resp))

def summarize_meeting_with_tags(text):
    prompt = (
        "Summarize this meeting transcript into:\n"
        "SUMMARY: key discussion points (5-6 bullet points)\n"
        "ACTION_ITEMS: tasks or follow-ups.\n"
        "Return plain text with these sections clearly marked."
    )
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, text])
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
