import os
import csv
from datetime import datetime


FEEDBACK_FILE = "data/user_feedback.csv"


def save_feedback(weather: dict, ml_prediction: dict, feedback_type: str):
    """
    Salvează feedback-ul utilizatorului într-un fișier CSV.

    feedback_type poate fi:
    - "colder"
    - "correct"
    - "warmer"
    """

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(FEEDBACK_FILE)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": weather.get("city", ""),
        "temperature": weather.get("temperature", ""),
        "api_feels_like": weather.get("feels_like", ""),
        "humidity": weather.get("humidity", ""),
        "pressure": weather.get("pressure", ""),
        "wind_speed": weather.get("wind_speed", ""),
        "clouds": weather.get("clouds", ""),
        "description": weather.get("description", ""),
        "ml_shadow_feels": ml_prediction.get("shadow_feels", ""),
        "ml_sun_feels": ml_prediction.get("sun_feels", ""),
        "comfort_score": ml_prediction.get("comfort_score", ""),
        "solar_radiation": ml_prediction.get("solar_radiation", ""),
        "feedback_type": feedback_type,
    }

    with open(FEEDBACK_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)