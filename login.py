import customtkinter as ctk
from pydexcom import Dexcom
import json
import subprocess
import sys
import os

app = ctk.CTk()
app.title("PyDex Login")
app.geometry("800x480")




ctk.set_default_color_theme("blue")

def login():
    username = username_entry.get()
    password = password_entry.get()
    print(username, password)
    try:
        dexcom = Dexcom(username=username, password=password, region="ous")
        get_reading = dexcom.get_current_glucose_reading()
        if get_reading != None:
            print(get_reading.mmol_l)
            reading = get_reading.mmol_l
            print(reading)
            test = True
            os.execv(sys.executable, ["python", "full.py", username, password])
            
        else:
            test = False
    except:
        test = False
    if test:
        pass
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

app.mainloop()