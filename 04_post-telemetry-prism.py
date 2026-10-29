


import requests
import sys
import json 
from pathlib import Path


with open("secrets.json") as secrets:
    secrets_data = json.load(secrets)

bearer_tokenPrism = secrets_data["prism_group"]["cobb_prism_key"]
url = 'https://api.adsprism.com/api/Telemetry'
headers = {
    "accept": "*/*",
    "x-ads-dev": bearer_tokenPrism,
    "Content-Type": "application/json-patch+json"
}

prism_payload = Path("prism_payload/")

for file in prism_payload.glob("prism_payload_*.json"):
    with open(file) as f:
        data = json.load(f)



    meter_name = file.stem.split("_")[-1]
    #with open("C:/Users/poovey/OneDrive - Woolpert/Documents/aaProjects/Ga_Rockdale/API/formatted-for-prism.json") as f:
    #    data = json.load(f)

    try: 
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        if response.status_code != 202:
            print(f"Error: Received status code {response.status_code}")
            sys.exit(1)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        sys.exit(1)
    except Exception as err:
        print(f"An error occured: {err}")
        sys.exit(1)

    if response.status_code == 202:
        print (f"Data for meter location {meter_name} (should've) successfully appended to PRISM!")
        print(response)


