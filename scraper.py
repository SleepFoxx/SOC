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
        
        lines = raw_data.strip().split('\n')
        
        for line in lines:
            parts = line.split()
            
            if len(parts) >= 4:  
                datetime_str = parts[0].strip('"')
                sgv_value = parts[2]
                
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                datetime_obj += timedelta(hours=1)
                time_part = datetime_obj.strftime('%H:%M')
                sgv_mmol = round(int(sgv_value) * 0.05551, 1)
                
                time_values.append(time_part)
                sgv_values.append(sgv_mmol)
        
        print("Time values:", time_values)
        print("SGV values:", sgv_values)
        return time_values, sgv_values

    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)
scrape()
