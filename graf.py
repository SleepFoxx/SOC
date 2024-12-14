import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pydexcom import Dexcom
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dexcom = Dexcom(username="sleepfox", password="Littlelam0412", region="ous")

times = []
values = []

history_glucose = []
history_time = []

plt.style.use('dark_background')

root = tk.Tk()
root.title("Glukózový graf")
root.geometry("320x240")

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlabel('Čas', fontsize=6)
ax.set_ylabel('Hodnota (napr. glukóza)', fontsize=6)
ax.set_ylim(3.5, 22.2)

sc = ax.scatter(times, values, color='b', marker='o', picker=True)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
ax.tick_params(axis='x', which='minor', length=4)

def update_graph():
    get_reading = dexcom.get_current_glucose_reading()
    glucose_value = round(get_reading.mmol_l, 1)

    values.append(glucose_value)
    current_time = datetime.now()
    times.append(current_time)

    if len(times) > 180:
        times.pop(0)
        values.pop(0)

    sc.set_offsets(list(zip(times, values)))

    ax.set_xlim([times[-1] - timedelta(hours=3) - timedelta(minutes=10), times[-1] + timedelta(minutes=10)])

    fig.canvas.draw_idle()

    root.after(300000, update_graph)

def on_pick(event):
    global history_glucose, history_time

    ind = event.ind
    if len(ind) > 0:
        for i in ind:
            time_clicked = times[i].strftime('%H:%M')
            value_clicked = values[i]

            if time_clicked not in history_time:
                history_glucose.append(value_clicked)
                history_time.append(time_clicked)

            info_label.config(text=f"{time_clicked}\n{value_clicked} mmol/L")
            info_label.place(x=150, y=20)

            root.after(10000, hide_info_text)

def hide_info_text():
    info_label.place_forget()

update_graph()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

info_label = tk.Label(root, text="Kliknite na bod na grafe", bg='black', fg='white', font=('Comic Sans', 10))
info_label.place(x=150, y=20)

fig.canvas.mpl_connect('pick_event', on_pick)

for label in ax.get_xticklabels():
    label.set_fontsize(8)

for label in ax.get_yticklabels():
    label.set_fontsize(6)

ax.yaxis.set_tick_params(labelleft=True, labelright=False)

root.mainloop()
