import requests
from datetime import datetime, timedelta


def scrape():
    base_url = "https://site--nightscout--m9xqnnmsqrfs.code.run/api/v1/entries"

    params = {
        "count": 36,  
        "sort": "-date"  
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        raw_data = response.text
        time_values = []
        sgv_values = []
        arrow_values = []
        
        lines = raw_data.strip().split('\n')
        
        for line in lines:
            parts = line.split()
            
            if len(parts) >= 4:  
                datetime_str = parts[0].strip('"')
                sgv_value = parts[2]
                arrow_value = parts[3].strip('"')

                match arrow_value:
                    case "Flat":
                        arrow_value = "→"
                    case "FortyFiveUp":
                        arrow_value = "↗"
                    case "SingleUp":
                        arrow_value = "↑"
                    case "DoubleUp":
                        arrow_value = "↑"
                    case "FortyFiveDown":
                        arrow_value = "↘"
                    case "SingleDown":
                        arrow_value = "↓"
                    case "DoubleDown":
                        arrow_value = "↓"
                    case _:
                        arrow_value = "→"
                
                
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                datetime_obj += timedelta(hours=1)
                time_part = datetime_obj.strftime('%H:%M')
                sgv_mmol = round(int(sgv_value) * 0.05551, 1)
                
                time_values.insert(0, time_part)
                sgv_values.insert(0, sgv_mmol)
                arrow_values.insert(0, arrow_value)
        
        return time_values, sgv_values, arrow_values

    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)
