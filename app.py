import customtkinter as ctk
from pydexcom import Dexcom


app = ctk.CTk()
app.title("PyDex App")
app.geometry("320x240")

ctk.set_default_color_theme("blue")


username = "sleepfox"
password = "Littlelam0412"
dexcom = Dexcom(username=username, password=password, region="ous")


frame = ctk.CTkFrame(master=app, width=300, height=200, corner_radius=15)
frame.pack(pady=20, padx=10, fill="both", expand=True)


glucose_label = ctk.CTkLabel(master=frame, text="", font=("Comic-sans", 25))
glucose_label.place(x=130, y=30)

arrow_label = ctk.CTkLabel(master=frame, text="", font=("Comic-sans", 25))
arrow_label.place(x=170, y=30)



def prepis():
    glucose_reading = dexcom.get_current_glucose_reading()


    glucose_label.configure(text=glucose_reading.mmol_l)
    arrow_label.configure(text=glucose_reading.trend_arrow)


    print(glucose_reading.mmol_l)
    print(glucose_reading.trend_arrow)


def update_glucose():
    prepis()  
    app.after(10000, update_glucose)  


update_glucose()

app.mainloop()
