

import requests
import json
import sys
import os

os.makedirs("prism_locations", exist_ok=True)


with open("secrets.json") as secrets:
    secrets_data = json.load(secrets)


#bearer_tokenPrism = 'fj8EWIy2Bx8oIbTfgsSCVergx/hzUWBQrtz1SxtlTck='
for key in secrets_data["prism_group"]:
    bearer_tokenPrism = secrets_data["prism_group"][key]


    url = 'https://api.adsprism.com/api/Locations'
    headers = {
        "accept": "text/plain",
        "x-ads-dev": bearer_tokenPrism
    }

    query = { 
        "showInactives": "True"
    }



    response = requests.get(url,headers=headers, params=query)
    response.raise_for_status()
    if response.status_code != 200:
        print(f"Error:  Received status code {response.status_code}")
        sys.exit(1)


    data = response.json()
    #print(data)
    with open (f"prism_locations/prism-location-list-{key}.json","w",encoding="utf-8") as file:
        json.dump(data,file,indent=2)
        