import sqlite3
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def init_db():
    conn = sqlite3.connect("hopeline.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        emotion TEXT,
        ai_response TEXT
    )''')
    conn.commit()
    conn.close()

def save_entry(user_input, emotion, ai_response):
    encrypted_input = cipher.encrypt(user_input.encode())
    encrypted_response = cipher.encrypt(ai_response.encode())
    conn = sqlite3.connect("hopeline.db")
    c = conn.cursor()
    c.execute("INSERT INTO entries (user_input, emotion, ai_response) VALUES (?, ?, ?)", 
              (encrypted_input, emotion, encrypted_response))
    conn.commit()
    conn.close()
