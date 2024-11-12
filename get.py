from pydexcom import Dexcom
from datetime import datetime
import schedule
import time

dexcom = Dexcom(username= "sleepfox", password= "Littlelam2", region="ous")

def zaznam():
    glucose_reading = dexcom.get_current_glucose_reading()
    print(glucose_reading.mmol_l)

def vypis_cas():
    print(datetime.now())

schedule.every(5).minutes.do(zaznam)
schedule.every(1).minutes.do(vypis_cas)

while True:
    schedule.run_pending()
    time.sleep(1)

