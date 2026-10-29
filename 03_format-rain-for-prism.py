

import json
import pandas as pd
from pathlib import Path 


rain_folder = Path("split_by_logger/")
entity_id = 2123

rain_gauge_to_meter_map = {
    "22546624": [1339],
    "22546626": [1342],
    "22546628": [1340],
    "22546627": [1337],
    "22546629": [1341],
    "22546632": [1344],
    "22546625": [1345],
    "22546630": [1343],
    "22546631": [1338],
    "22546633": [1336]
}

for file in rain_folder.glob("rain_*.json"):
    with open(file) as f:
        rain_data = json.load(f)["data"]

    df = pd.DataFrame(rain_data)

    df["dateTime"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    rg_name = file.stem.replace("rain_","").replace("_", " ")

    location_ids = rain_gauge_to_meter_map.get(rg_name, [])

    for loc_id in location_ids:
        output = [{
            "entityID": entity_id,
            "locationID": loc_id,
            "data": [
                {
                    "dateTime": row["dateTime"],
                    "reading": row["value"]
                }
                for _, row in df.iterrows()
            ]
        }]

        output_dir = Path("prism_payload/")
        output_dir.mkdir(exist_ok=True)
        out_filename = f"{output_dir}/prism_payload_{rg_name}_loc{loc_id}.json"
        with open(out_filename, "w") as f:
            json.dump(output, f, indent=2)
            print(f"Created: prism_payload_{rg_name}_loc{loc_id}.json")

