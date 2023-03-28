import requests
import csv

xmin = -30
xmax = 40
ymin = 28
ymax = 73

# API endpoint URL
url = "https://api.openweathermap.org/data/2.5/weather"

wind_speeds = []

for lon in range(xmin, xmax):
    for lat in range(ymin, ymax):
        # API parameters
        params = {
            "lon": lon,     # Query for Europe
            "lat": lat,
            "appid": "11741b2d1a55e57d579f35fef71586db",    # Replace with your API key
            "units": "metric"  # Use metric units for wind speed in meters per second
        }

        # Send API request
        response = requests.get(url, params=params)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            wind_speeds.append([(lon, lat), data["wind"]["speed"]])
        else:
            print("Error:", response.status_code)

with open("data/windspeeds.csv", "w") as f:
    writer = csv.writer(f)
    for row in wind_speeds:
        writer.writerow(row)