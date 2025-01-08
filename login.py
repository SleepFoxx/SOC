import customtkinter as ctk
from pydexcom import Dexcom
import json
import subprocess
import sqlite3
import hashlib
import sys
import os

def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

app = ctk.CTk()
app.title("PyDex Login")
app.geometry("800x480")


def hash_password(password):
    salt = os.urandom(32) 
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed 

def verify_password(stored_password, provided_password):
    stored_password = bytes.fromhex(stored_password)
    salt, stored_hash = stored_password[:32], stored_password[32:]
    hashed_attempt = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return hashed_attempt == stored_hash

def save_user(username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False  
    hashed_password = hash_password(password).hex()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    return True


ctk.set_default_color_theme("blue")

def login():
    username = username_entry.get()
    password = password_entry.get()
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    data = Dexcom(username=username, password=password, region="ous")
    glucose_reading = data.get_current_glucose_reading()
    
    if user and verify_password(user[0], password):
        status_label.configure(text="Login successful")
        os.execv(sys.executable, ["python", "full.py", username, password])
    elif glucose_reading != None:
        save_user(username, password)
        status_label.configure(text="Login successful")
        os.execv(sys.executable, ["python", "full.py", username, password])
    else:
        status_label.configure(text="Login failed")


frame = ctk.CTkFrame(master=app, width=780, height=460, corner_radius=15)
frame.pack(pady=10, padx=10, fill="both", expand=True)

login_label = ctk.CTkLabel(master=frame, text="Login", font=("Arial", 24))
login_label.pack(pady=30)

username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", font=("Arial", 18), height=40, width=300)
username_entry.pack(pady=15, padx=20)

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", font=("Arial", 18), height=40, width=300)
password_entry.pack(pady=15, padx=20)

login_button = ctk.CTkButton(master=frame, text="Login", command=login, font=("Arial", 18), width=300, height=40)
login_button.pack(pady=20)

status_label = ctk.CTkLabel(master=frame, text="", font=("Arial", 14))
status_label.pack(pady=10)



app.mainloop()

