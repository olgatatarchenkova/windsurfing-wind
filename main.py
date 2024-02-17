import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Dahab, UTC + 2
LATITUDE = 34.501560
LONGITUDE = 28.488930
OMW_Endpoint = os.getenv('OMW_END')
API_KEY = os.getenv('API_KEY')
UTC = 2


def wind_direction(wind_deg):
    if wind_deg <= 25:
        direct = "N"
    elif 25 < wind_deg <= 65:
        direct = "NE"
    elif 65 < wind_deg <= 115:
        direct = "E"
    elif 115 < wind_deg <= 155:
        direct = "SE"
    elif 155 < wind_deg <= 205:
        direct = "S"
    elif 205 < wind_deg <= 245:
        direct = "SW"
    elif 245 < wind_deg <= 295:
        direct = "W"
    elif 295 < wind_deg <= 335:
        direct = "NW"
    else:
        direct = "N"
    return direct


def time_converter(time_utc):
    # UTC time string
    utc_time_string = time_utc

    # Convert UTC time string to datetime object
    utc_time = datetime.strptime(utc_time_string, "%Y-%m-%d %H:%M:%S")

    # Add 2 hours to the datetime object to convert to UTC+2
    utc_plus_2_time = utc_time + timedelta(hours=UTC)

    # Convert the UTC+2 time back to a string
    utc_plus_2_time_string = utc_plus_2_time.strftime("%Y-%m-%d %H:%M:%S")

    # print(utc_plus_2_time_string)
    return utc_plus_2_time_string


def format_message(message):
    replacements = {
        "speed": "Speed (m/s)",
        "deg": "Direction",
        "gust": "Gusts (m/s)",
        "all": "Clouds",
        "{": "",
        "}": "",
        "'": ""
    }
    for old, new in replacements.items():
        message = message.replace(old, new)
    return message


parameters = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 4,
    }

try:
    response = requests.get(url=OMW_Endpoint, params=parameters)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Error occurred:", e)

wind = False

for hour_data in data["list"]:
    dt_txt = hour_data["dt_txt"]
    dt_txt2 = time_converter(dt_txt)
    hour_data["wind"]["deg"] = wind_direction(hour_data["wind"]["deg"])
    if 7 <= int(hour_data["wind"]["speed"]) <= 13:
        wind = True
        print(f"Happy Windsurfing!\n")
        message = ""
        message += f"{dt_txt2}\n{hour_data["wind"]}\n{hour_data["clouds"]} %\nHumidity: {hour_data["main"]["humidity"]} %\n\n"
        message = format_message(message)
        print(message)

if not wind:
    print(f"Go Diving!\n")
