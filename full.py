import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pydexcom import Dexcom
import sys
from PIL import Image, ImageTk
from scraper import *
#from prediction import generate_predictions
import pygame
import os
from collections import deque




username = sys.argv[1]
password = sys.argv[2]

dexcom = Dexcom(username=username, password=password, region="ous")

app = ctk.CTk()
app.title("PyDexcom")
app.attributes("-fullscreen", True)
app.geometry("800x480")
app.configure(bg="#000000")

ctk.set_default_color_theme("sources/themes/black.json")

frame_info = ctk.CTkFrame(master=app, width=800, height=160, corner_radius=5, fg_color="#000000")
frame_info.pack(pady=0, padx=0, fill="x")

glucose_label = ctk.CTkLabel(master=frame_info, text="", font=("Comic-sans", 25), fg_color="#000000", text_color="white")
arrow_label = ctk.CTkLabel(master=frame_info, text="", font=("Comic-sans", 25), fg_color="#000000", text_color="white")

image_label = ctk.CTkLabel(master=frame_info, image="", text="", compound="center", font=("Comic-sans", 23), fg_color="#000000", text_color="white")
image_label.place(x=330, y=40)

mute_button = None
mute_until = None



frame_graph = ctk.CTkFrame(master=app, corner_radius=1, fg_color="#000000")
frame_graph.pack(pady=0, padx=0, fill="both", expand=True)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(bottom=0.2)  

ax.set_xlabel('Čas', fontsize=10, color="white")
ax.set_ylabel('Glykémia (mmol/L)', fontsize=10, color="white")
ax.set_ylim(2.2, 22.2)
sc = ax.scatter([], [], color='white', marker='o', picker=True)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))

ax.axhline(y=4.0, color='red', linestyle='--', linewidth=1, label="Dolná hranica (4 mmol/L)")
ax.axhline(y=12.0, color='yellow', linestyle='--', linewidth=1, label="Horná hranica (12 mmol/L)")

canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

times = []
values = []
arrows = []
times, values, arrows = scrape()

def mute_alert():
    global mute_until, mute_button
    mute_until = datetime.now() + timedelta(minutes=30)
    if mute_button:
        pygame.mixer.music.stop()
        mute_button.place_forget()
        pygame.mixer.music.unload()

def show_mute_button():
    global mute_button
    if not mute_button:
        pygame.mixer.init()
        pygame.mixer.music.play()
        mute_button = ctk.CTkButton(master=app, text="Stíšiť", command=mute_alert, border_width=2, border_color="grey")
        mute_button.place(x=10, y=10)  
        mute_button.lift()  

def update_glucose(on_clicking=False, first = False):
    global mute_until
    try:
        glucose_reading = dexcom.get_current_glucose_reading()
        glucose_value = round(glucose_reading.mmol_l, 1)

        if glucose_value > 12.0:
            glucose_label.configure(text_color="yellow")
            image_label.configure(text_color="yellow")
            if not mute_until or datetime.now() > mute_until:
                pygame.mixer.init()
                pygame.mixer.music.load("sources/sounds/high_alert.mp3")
                show_mute_button()
        elif glucose_value < 4.0:
            glucose_label.configure(text_color="red")
            image_label.configure(text_color="red")
            if not mute_until or datetime.now() > mute_until:
                pygame.mixer.init()
                pygame.mixer.music.load("sources/sounds/low_alert.mp3")
                show_mute_button()
                show_mute_button()
        else:
            glucose_label.configure(text_color="white")
            image_label.configure(text_color="white")

        glucose_label.configure(text=f"{glucose_value}")
        image_label.configure(text = f"{glucose_value}")
        match glucose_reading.trend_arrow:
            case "→":
                image = Image.open("sources/images/straight_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=320, y=40)
                image_label.configure(image = photo)
            case "↑":
                image = Image.open("sources/images/up_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=330, y=10)
                image_label.configure(image = photo)
            case "↓":
                image = Image.open("sources/images/down_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=340, y=-5)
                image_label.configure(image = photo)
            case "↗":
                image = Image.open("sources/images/up_right_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=315, y=30)
                image_label.configure(image = photo)
            case "↘":
                image = Image.open("sources/images/down_right_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=320, y=25)
                image_label.configure(image = photo)
            case _:
                image = Image.open("sources/images/straight_white_small.png")
                photo = ImageTk.PhotoImage(image)
                image_label.place(x=320, y=40)
                image_label.configure(image = photo)
        if on_clicking == False:
            values.append(glucose_value)
            current_time = datetime.now()
            formated_time = current_time.strftime('%H:%M')  
            times.append(formated_time)
            time_objects = [datetime.strptime(t, '%H:%M') for t in times]
            """
            if(first == False):
                for i in range (27, 37):
                    times.pop(i)
                    values.pop(i)
            
            predictions, predictions_downward, predicted_times = generate_predictions(5)

            predicted_times_objects = [datetime.strptime(t, '%H:%M') for t in predicted_times]
            

            for i in range(len(predictions)):
                values.append( predictions[i])
                values.append( predictions_downward[i])
                times.append(predicted_times[i])
                times.append(predicted_times[i])
            """
            if len(times) > 36:
                times.pop(0)
                values.pop(0)
            """
            
            for i in range(len(values)):
                if i >= len(values) - 2 * len(predicted_times):
                    colors.append('blue')
                elif values[i] > 12.0:
                    colors.append('yellow')
                elif values[i] < 4.0:
                    colors.append('red')
                else:
                    colors.append('white')
            """
            colors = ['yellow' if v > 12.0 else 'red' if v < 4.0 else 'white' for v in values]

            sc.set_offsets(list(zip(mdates.date2num(time_objects), values)))
            sc.set_color(colors)

            ax.set_xlim([time_objects[-1] - timedelta(hours=3), time_objects[-1] + timedelta(minutes=10)])
            fig.canvas.draw_idle()
    except Exception as e:
        glucose_label.configure(text="Chyba")
        arrow_label.configure(text=str(e))
    if(on_clicking == False):
        app.after(300000, update_glucose)  

def on_pick(event):
    ind = event.ind
    if len(ind) > 0:
        i = ind[0]
        time_clicked = times[i]
        value_clicked = values[i]

        glucose_label.place(relx=0.5, rely=0.4, anchor="center")
        glucose_label.configure(text=f"{value_clicked} mmol/L")

        arrow_label.place(relx=0.5, rely=0.7, anchor="center")
        if value_clicked > 12.0:
            glucose_label.configure(text_color="yellow")
        elif value_clicked < 4.0:
            glucose_label.configure(text_color="red")
        else:
            glucose_label.configure(text_color="white")
        arrow_label.configure(text=f"Kliknuté: {time_clicked}")

        image_label.place_forget()

        def restore_original_text():
            glucose_label.configure(text="")
            glucose_label.place_forget()

            arrow_label.configure(text="")
            arrow_label.place_forget()
            
            image_label.place(x=330, y=40)
            update_glucose(on_clicking=True)

        app.after(5000, restore_original_text)

def shutdown_system():
    os.system("sudo shutdown now")

power_icon = Image.open("sources/images/power_button.png")
power_icon = power_icon.resize((40, 40))
power_photo = ImageTk.PhotoImage(power_icon)

power_button = ctk.CTkButton(master=app, text = "", image=power_photo, command=shutdown_system, fg_color="black", hover_color="black", border_width=0, corner_radius=0, width=40, height=40)
power_button.place(x=700, y=10)

def on_closing():
    app.quit()  
    app.destroy()  
app.protocol("WM_DELETE_WINDOW", on_closing)

fig.canvas.mpl_connect('pick_event', on_pick)

info_label = ctk.CTkLabel(master=app, text="Kliknite na bod na grafe", font=("Comic-sans", 15), fg_color="#000000", text_color="white")
info_label.pack()

update_glucose(first = True)

app.mainloop()
