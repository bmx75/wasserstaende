import requests
import pandas as pd
import time

# Datei mit den gewünschten Pegeln
stations_file = "stations.csv"

# PEGELONLINE API
api_url = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json"

# gewünschte Pegel laden
stations = pd.read_csv(stations_file)

# alle verfügbaren Stationen abrufen
response = requests.get(api_url, timeout=30)
response.raise_for_status()

all_stations = response.json()

results = []

for _, row in stations.iterrows():

    search_name = row["pegel"].lower()

    found = None

    # passenden Pegel suchen
    for station in all_stations:
        name = station.get("shortname", "").lower()

        if search_name in name:
            found = station
            break

    if found:

        station_id = found["uuid"]

        # aktuellen Messwert für diese Station holen
        detail_url = (
            f"https://www.pegelonline.wsv.de/"
            f"webservices/rest-api/v2/stations/"
            f"{station_id}.json?includeCurrentMeasurement=true"
        )

        detail = requests.get(detail_url, timeout=30).json()

        measurement = detail.get("currentMeasurement")

        if measurement:

            results.append({
                "Pegel": row["pegel"],
                "Fluss": row["fluss"],
                "Wasserstand_cm": measurement.get("value"),
                "Zeit": measurement.get("timestamp"),
                "Latitude": found.get("latitude"),
                "Longitude": found.get("longitude")
            })

    # kleine Pause, damit die API nicht unnötig belastet wird
    time.sleep(0.2)


# Ergebnis speichern
df = pd.DataFrame(results)

df.to_csv(
    "pegel.csv",
    index=False,
    encoding="utf-8"
)

print("Fertig. Pegel gespeichert:", len(df))
