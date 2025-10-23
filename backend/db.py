import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "meetings.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create meetings table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            attendees TEXT,
            transcript TEXT,
            summary TEXT,
            people TEXT,
            action_items TEXT,
            created_at TEXT
        )
    ''')

    # Create sessions table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            context TEXT,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()
