import requests
import pandas as pd

url = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json"

response = requests.get(url, timeout=30)
response.raise_for_status()

stations = response.json()

rows = []

for station in stations:
    rows.append({
        "Pegel": station.get("shortname"),
        "Gewässer": station.get("water", {}).get("shortname"),
        "Latitude": station.get("latitude"),
        "Longitude": station.get("longitude")
    })

df = pd.DataFrame(rows)

df.to_csv("pegel.csv", index=False)

print(df.head())
