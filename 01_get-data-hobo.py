


import requests
import sys
import json
import pandas as pd
from datetime import datetime, timezone, timedelta
from pathlib import Path


with open("secrets.json") as secrets:
    secrets_data = json.load(secrets)


bearer_tokenHobo = secrets_data["likor_group"]["likor_key"] #added this on 2026-10-27 to remove keys from commits
url = 'https://api.licor.cloud/v1/data'   #new API end point as of 7/2/2025
headers = {
    "Authorization": f"Bearer {bearer_tokenHobo}",
    'accept': 'application/json'
}


with open("logger_sn.json") as file:    #open the list of hobo logger sn's 
    data = json.load(file)

logger_sns = [entry["logger_sn"] for entry in data["data"]]    #create a local list of the logger sns


time_now_utc = datetime.now(tz=timezone.utc)            #TODO Need to configure this... call down the last 24 hours? only ~400 records... 
start_date_time = (time_now_utc - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
#start_date_time_formatted = 
end_date_time = "2040-01-01 04:20:00"          #i'll fix this in 2040

for logger in logger_sns:       
    query = {
        'loggers': logger,
        'start_date_time': start_date_time,
        'end_date_time': end_date_time
    }

    #standard block
    try: 
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        
    except Exception as err:
        print(f"An error occured: {err}")
        

    if response.status_code == 200: 
        print ("Request was successful!")

        data = response.json()
        if data["message"] != "":

            output_files = []
            output_dir = Path("split_by_logger/")
            output_dir.mkdir(exist_ok=True)
            with open(f"split_by_logger/get-data-raw-hobo_{logger}.json", "w") as file:
                json.dump(data,file,indent=4)
                print(f"Raw response json saved for: {logger}")
            #raw_data= json.load(data)
            df = pd.DataFrame(data["data"])
            rain_df = df[df["sensor_measurement_type"].str.lower() == "rain"].copy()
            rain_df["entityID"] = "2123"

            for logger_sn, group in rain_df.groupby("logger_sn"):
                filename_json = output_dir / f"rain_{logger_sn}.json"
                #save as json
                with open(filename_json,"w") as f:
                    json.dump({"data": group.to_dict(orient="records")}, f, indent=2)
                print(f'Saved JSON: {filename_json}')

                filename_csv  = output_dir / f'rain_{logger_sn}.csv'
                group_csv = group.copy()
                group_csv["timestamp"] = (
                    pd.to_datetime(group_csv["timestamp"], utc=True)
                    .dt.tz_convert("ETC/GMT+5") # inverted minus to + ignores DST?? confirm
                    .dt.strftime("%Y-%m-%d %H:%M:%S")
                )
                #save as csv
                group_csv.to_csv(filename_csv, index=False)
                print(f'Saved CSV: {filename_csv}')
        else:
            print(f"No data returned for logger: {logger}")

       
################## Run the others ####################
exec(open(f"03_format-rain-for-prism.py").read())
exec(open(f"04_post-telemetry-prism.py").read())

print("The Cobb script has completed. Go home. ")
