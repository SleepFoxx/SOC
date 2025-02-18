import customtkinter as ctk
from pydexcom import Dexcom
import sqlite3
import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



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


def generate_key():
    if not os.path.exists("test.txt"):
        key = get_random_bytes(32)
        with open("test.txt", "wb") as f:
            f.write(key)

def load_key():
    with open("test.txt", "rb") as f:
        return f.read()


def encrypt_password(password):
    key = load_key()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()


def decrypt_password(encrypted_password):
    key = load_key()
    data = base64.b64decode(encrypted_password)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()


def save_user(username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    encrypted_password = encrypt_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
    conn.commit()
    conn.close()
    return True




def login():
    username = username_entry.get()
    password = password_entry.get()
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        try:
            stored_password = decrypt_password(user[0])
            if stored_password == password:
                status_label.configure(text="Login successful")
                os.execv(sys.executable, [sys.executable, "full.py", username, password])
                return
        except:
            pass
    
    try:
        data = Dexcom(username=username, password=password, region="ous")
        glucose_reading = data.get_current_glucose_reading()
        if glucose_reading:
            save_user(username, password)
            status_label.configure(text="Login successful")
            os.execv(sys.executable, [sys.executable, "full.py", username, password])
            return
    except:
        pass

    status_label.configure(text="Login failed")


init_db()
generate_key()
os.environ["DISPLAY"] = ":0"

app = ctk.CTk()
app.title("Login")
ctk.set_default_color_theme("blue")
app.geometry("800x480")

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

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

for data in cursor.execute("SELECT username, password FROM users"):
    username, stored_password = data
    def quick_login(username=username, stored_password=stored_password):
        decrypted_password = decrypt_password(stored_password)
        os.execv(sys.executable, [sys.executable, "full.py", username, decrypted_password])
    
    quick_login_button = ctk.CTkButton(
        master=frame, text=username, command=quick_login, font=("Arial", 14), width=280, height=40
    )
    quick_login_button.pack(pady=5, padx=20)

conn.close()

app.mainloop()
