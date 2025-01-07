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


frame = ctk.CTkFrame(master=app, width=300, height=200, corner_radius=15)
frame.pack(pady=20, padx=10, fill="both", expand=True)

login_label = ctk.CTkLabel(master=frame, text="Login", font=("Arial", 18))
login_label.pack(pady=10)

username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
username_entry.pack(pady=5, padx=10)

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=5, padx=10)

login_button = ctk.CTkButton(master=frame, text="Login", command=login)
login_button.pack(pady=10)

status_label = ctk.CTkLabel(master=frame, text="", font=("Arial", 10))
status_label.pack(pady=5)

app.mainloop()