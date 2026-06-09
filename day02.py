import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
CITIES = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Tirunelveli", "Madurai", "Theni"]
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "India_Weather_Major_Cities.csv")

def extract(city: str, api_key: str) -> dict:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Extracted weather data for {city}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error for {city}: {e}")
        return {}
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection error for {city}")
        return {}

def transform(data: dict) -> dict:
    try:
        feels_like = data["main"]["feels_like"]

        # Categorise heat index
        if feels_like < 27:
            heat_index = "Comfortable"
        elif feels_like < 32:
            heat_index = "Warm"
        elif feels_like < 38:
            heat_index = "Hot"
        elif feels_like < 45:
            heat_index = "Very Hot"
        else:
            heat_index = "Dangerous"

        return {
            "city"          : data["name"],
            "temperature_c" : data["main"]["temp"],
            "feels_like_c"  : feels_like,
            "humidity_pct"  : data["main"]["humidity"],
            "weather"       : data["weather"][0]["description"],
            "wind_speed"    : data["wind"]["speed"],
            "heat_index"    : heat_index,
            "extracted_at"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except KeyError as e:
        logging.error(f"Missing field: {e}")
        return {}

def load(records: list, filepath: str):
    try:
        df_new = pd.DataFrame(records)
        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
            logging.info(f"Appended {len(df_new)} rows - total row {len(df_final)} rows")
        else:
            df_final = df_new
            logging.info(f"Created new file with {len(df_final)} rows")
        df_final.to_csv(filepath, index=False)
        return df_final
    except Exception as e:
        logging.error(f"Load failed: {e}")
        return pd.DataFrame()

def summarise(df: pd.DataFrame):
    try:
        hottest_idx = df['temperature_c'].idxmax()
        coolest_idx = df['temperature_c'].idxmin()
        humid_idx   = df['humidity_pct'].idxmax()
        print("\n=== India Weather Summary ===")
        print(f"Total cities tracked : {len(df)}")
        print(f"Hottest city         : {df.loc[hottest_idx, 'city']} ({df.loc[hottest_idx, 'temperature_c']}°C)")
        print(f"Coolest city         : {df.loc[coolest_idx, 'city']} ({df.loc[coolest_idx, 'temperature_c']}°C)")
        print(f"Most humid city      : {df.loc[humid_idx, 'city']} ({df.loc[humid_idx, 'humidity_pct']}%)")
        print(f"Average temperature  : {df['temperature_c'].mean().round(1)}°C")
        print("=============================\n")
    except Exception as e:
        logging.error(f"Summarise failed: {e}")

def run_pipeline():
    logging.info("=== Weather pipeline started ===")
    records = []
    for city in CITIES:
        raw = extract(city, API_KEY)
        if raw:
            record = transform(raw)
            if record:
                records.append(record)
    df_final = load(records, OUTPUT_FILE)
    summarise(df_final)
    logging.info("=== Weather pipeline completed ===")

run_pipeline()
