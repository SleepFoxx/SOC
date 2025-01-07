import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pydexcom import Dexcom
import sys

username = sys.argv[1]
password = sys.argv[2]

dexcom = Dexcom(username=username, password=password, region="ous")

app = ctk.CTk()
app.title("PyDex App")
app.geometry("800x480")
app.configure(bg="#000000")

ctk.set_default_color_theme("black.json")


frame_info = ctk.CTkFrame(master=app, width=800, height=150, corner_radius=15, fg_color="#000000")
frame_info.pack(pady=20, padx=10, fill="x")

glucose_label = ctk.CTkLabel(master=frame_info, text="", font=("Comic-sans", 25), fg_color="#000000", text_color="white")
glucose_label.place(relx=0.5, rely=0.4, anchor="center")

arrow_label = ctk.CTkLabel(master=frame_info, text="", font=("Comic-sans", 25), fg_color="#000000", text_color="white")
arrow_label.place(relx=0.5, rely=0.7, anchor="center")

frame_graph = ctk.CTkFrame(master=app, corner_radius=15, fg_color="#000000")
frame_graph.pack(pady=20, padx=10, fill="both", expand=True)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlabel('Čas', fontsize=10, color="white")
ax.set_ylabel('Glukóza (mmol/L)', fontsize=10, color="white")
ax.set_ylim(3.5, 22.2)
sc = ax.scatter([], [], color='b', marker='o', picker=True)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))

canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

times = []
values = []

def update_glucose():
    try:
        glucose_reading = dexcom.get_current_glucose_reading()
        glucose_value = round(glucose_reading.mmol_l, 1)

        glucose_label.configure(text=f"{glucose_value} mmol/L")
        arrow_label.configure(text=glucose_reading.trend_arrow)

        values.append(glucose_value)
        current_time = datetime.now()
        times.append(current_time)

        if len(times) > 400:
            times.pop(0)
            values.pop(0)

        sc.set_offsets(list(zip(mdates.date2num(times), values)))
        ax.set_xlim([times[-1] - timedelta(hours=3), times[-1] + timedelta(minutes=10)])
        fig.canvas.draw_idle()

    except Exception as e:
        glucose_label.configure(text="Chyba")
        arrow_label.configure(text=str(e))

    app.after(300000, update_glucose)

def on_pick(event):
    ind = event.ind
    if len(ind) > 0:
        i = ind[0]
        time_clicked = times[i].strftime('%H:%M')
        value_clicked = values[i]

        original_glucose = glucose_label.cget("text")
        original_arrow = arrow_label.cget("text")

        glucose_label.configure(text=f"{value_clicked} mmol/L")
        arrow_label.configure(text=f"Kliknuté: {time_clicked}")

        def restore_original_text():
            glucose_label.configure(text=original_glucose)
            arrow_label.configure(text=original_arrow)

        app.after(10000, restore_original_text)

fig.canvas.mpl_connect('pick_event', on_pick)

info_label = ctk.CTkLabel(master=app, text="Kliknite na bod na grafe", font=("Comic-sans", 15), fg_color="#000000", text_color="white")
info_label.pack()

update_glucose()

app.mainloop()
