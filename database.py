import sqlite3
from config import Config
import contextlib

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with contextlib.closing(get_db_connection()) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    input_text TEXT,
                    source_url TEXT,
                    prediction TEXT,
                    confidence INTEGER,
                    explanation TEXT,
                    sources_json TEXT,
                    keywords_json TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

def create_user(username, password_hash):
    with contextlib.closing(get_db_connection()) as conn:
        with conn:
            try:
                cursor = conn.execute(
                    'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    (username, password_hash)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None # Username exists

def get_user_by_username(username):
    with contextlib.closing(get_db_connection()) as conn:
        cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id):
    with contextlib.closing(get_db_connection()) as conn:
        cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def save_prediction(input_text, source_url, prediction, confidence, explanation, sources_json, keywords_json, user_id=None):
    with contextlib.closing(get_db_connection()) as conn:
        with conn:
            cursor = conn.execute(
                'INSERT INTO history (user_id, input_text, source_url, prediction, confidence, explanation, sources_json, keywords_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, input_text, source_url, prediction, confidence, explanation, sources_json, keywords_json)
            )
            return cursor.lastrowid

def get_history(user_id=None, limit=50):
    with contextlib.closing(get_db_connection()) as conn:
        if user_id:
            cursor = conn.execute('SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', (user_id, limit))
        else:
            cursor = conn.execute('SELECT * FROM history ORDER BY timestamp DESC LIMIT ?', (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_prediction_by_id(pred_id):
    with contextlib.closing(get_db_connection()) as conn:
        cursor = conn.execute('SELECT * FROM history WHERE id = ?', (pred_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
