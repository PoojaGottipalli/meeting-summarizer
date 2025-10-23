# 🎧 Meeting Summarizer

An intelligent **AI-powered Meeting Summarization System** built with **Flask**, **SQLite**, and **Gemini AI**.  
This web application allows users to upload meeting audio files, transcribe them into text, and generate concise summaries and actionable insights automatically.

---

## 🚀 Features

- 🎤 Upload meeting **audio files** (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`)
- 🧠 **Automatic transcription** using Gemini ASR
- 📝 **Summarization** with key points, decisions, and highlights
- ✅ **Action item extraction** from meeting discussion
- 🕒 Stores each meeting record in **SQLite database**
- 💾 **Downloadable transcripts** and summaries
- 💻 Simple, modern **frontend interface**
- 🔒 Environment-based configuration using `.env`

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Flask (Python) |
| Database | SQLite |
| AI Model | Google Gemini 2.5 Flash |
| Frontend | HTML, CSS, JavaScript |
| File Handling | Werkzeug + Flask Upload |
| Environment | python-dotenv |

---

## 🏗️ Project Structure

meeting-summarizer/
│
├── backend/
│ ├── app.py # Flask entry point
│ ├── db.py # SQLite database setup
│ ├── llm.py # Gemini API integration
│ ├── routes/
│ │ ├── meeting.py # Meeting upload + processing routes
│ │ └── sessions.py # Optional future extension
│ ├── uploads/ # Temporary uploaded audio files
│ └── .env # Environment variables
│
├── frontend/
│ ├── templates/
│ │ ├── index.html # Upload page
│ │ └── meetings.html # Meeting summary display page
│ └── static/ # CSS, JS, assets
│
├── meetings.db # SQLite database file
├── .gitignore
├── README.md
└── requirements.txt

---

## ⚙️ Environment Setup

### 1️⃣ Create `.env` in your `backend` folder
```env
# Flask secret key for session management
FLASK_SECRET=your-secret-key-here

# Google Gemini API Key (from https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-api-key

# Upload folder path
UPLOAD_FOLDER=uploads

# Flask environment
FLASK_ENV=development

🧱 Installation & Run Locally
1️⃣ Clone the repository
bash
Copy code
git clone https://github.com/<your-username>/meeting-summarizer.git
cd meeting-summarizer/backend
2️⃣ Create virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate       # (Windows)
# or
source venv/bin/activate    # (Mac/Linux)
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Flask server
bash
Copy code
python app.py
5️⃣ Open the app
Visit 👉 http://127.0.0.1:5000/ in your browser

🎯 API Endpoints
Endpoint	Method	Description
/api/v1/upload	POST	Uploads an audio file and processes it
/api/v1/meetings/<id>	GET	Displays meeting transcript and summary
/uploads/<filename>	GET	Fetches uploaded file

🧠 How It Works
User uploads a meeting audio file.

Flask backend temporarily stores the file in /uploads.

Gemini API is used to:

Generate a verbatim transcript

Create a summary of the discussion

Extract action items

Results are stored in meetings.db (SQLite).

User can view or download summaries and transcripts.

🎨 Frontend UI
Clean, minimalist upload interface

Animated drag-and-drop upload box

Summary, transcript, and action items displayed with sectioned layout

Themed in green and white for a professional look

🧩 Example Output
🗒️ Summary

Puja completed and tested the new authentication module.

Arjun will finish API testing for the AI summarizer.

Deployment planned after successful testing.

Puja to document endpoints.

No blockers reported.

✅ Action Items

Arjun: Complete API testing.

Puja: Document API endpoints.

John: Schedule final review meeting.

🗣️ Transcript

John: Good morning everyone...
Puja: I’ve completed the new authentication module...

🧑‍💻 Developers
Your Name — Developer & Maintainer

Built with ❤️ using Flask, SQLite, and Gemini AI

☁️ Deployment (Optional)
You can deploy easily on:

Render — Flask backend hosting

Vercel / Netlify — Frontend hosting
Make sure to set environment variables for your backend in Render.

🛡️ License
This project is licensed under the MIT License — free for personal and academic use.

📬 Support
If you encounter issues or want to contribute:

Open an Issue on GitHub

Or reach out via email — your-email@example.com

