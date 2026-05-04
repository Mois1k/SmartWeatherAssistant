import os
import joblib
import pandas as pd
from datetime import datetime


MODEL_PATH = "models/weather_model.pkl"


class MLModelError(Exception):
    pass


def estimate_solar_radiation(clouds: float, hour: int) -> float:
    """
    Estimare simplificată pentru radiația solară.
    Mai târziu putem lua această valoare dintr-un API mai avansat.
    """
    is_day = 1 if 7 <= hour <= 20 else 0

    if not is_day:
        return 0

    sun_factor = max(0, 1 - clouds / 100)

    # Soarele este mai puternic în jurul prânzului
    noon_factor = max(0, 1 - abs(hour - 13) / 7)

    return sun_factor * noon_factor * 850


def get_comfort_score(
    shadow_feels: float,
    sun_feels: float,
    wind_speed: float,
    humidity: float
) -> int:
    """
    Scor de confort între 0 și 100.
    """
    avg_feels = (shadow_feels + sun_feels) / 2

    score = 100

    if avg_feels < 0:
        score -= 45
    elif avg_feels < 10:
        score -= 25
    elif avg_feels > 35:
        score -= 45
    elif avg_feels > 30:
        score -= 25

    if humidity > 80:
        score -= 15

    if wind_speed > 10:
        score -= 15

    return max(0, min(100, int(score)))


def generate_recommendation(
    shadow_feels: float,
    sun_feels: float,
    comfort_score: int
) -> str:
    if comfort_score >= 80:
        return "Vreme confortabilă. Este o perioadă bună pentru activități afară."

    if sun_feels >= 35:
        return "La soare se va simți foarte cald. Evită expunerea directă și caută umbră."

    if shadow_feels <= 5:
        return "Se simte rece chiar și la umbră. Ai grijă la vânt și temperatură scăzută."

    if comfort_score < 50:
        return "Confort termic scăzut. Ieși afară doar dacă este necesar sau alege o oră mai potrivită."

    return "Vreme acceptabilă, dar verifică diferența dintre soare și umbră."


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise MLModelError(
            "Modelul ML nu există. Rulează mai întâi: python3 train_model.py"
        )

    return joblib.load(MODEL_PATH)


def predict_single_weather_feel(weather: dict, hour: int, month: int) -> dict:
    """
    Primește un dicționar meteo și estimează:
    - temperatura resimțită la umbră
    - temperatura resimțită la soare
    - scor confort
    - recomandare
    """

    model = load_model()

    is_day = 1 if 7 <= hour <= 20 else 0

    solar_radiation = estimate_solar_radiation(
        clouds=weather["clouds"],
        hour=hour
    )

    input_data = pd.DataFrame([{
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],
        "clouds": weather["clouds"],
        "hour": hour,
        "month": month,
        "is_day": is_day,
        "solar_radiation": solar_radiation,
    }])

    prediction = model.predict(input_data)[0]

    shadow_feels = round(float(prediction[0]), 1)
    sun_feels = round(float(prediction[1]), 1)

    comfort_score = get_comfort_score(
        shadow_feels=shadow_feels,
        sun_feels=sun_feels,
        wind_speed=weather["wind_speed"],
        humidity=weather["humidity"],
    )

    recommendation = generate_recommendation(
        shadow_feels=shadow_feels,
        sun_feels=sun_feels,
        comfort_score=comfort_score,
    )

    return {
        "shadow_feels": shadow_feels,
        "sun_feels": sun_feels,
        "comfort_score": comfort_score,
        "recommendation": recommendation,
        "solar_radiation": round(solar_radiation, 1),
    }


def predict_weather_feel(weather: dict) -> dict:
    """
    Predicție ML pentru vremea actuală.
    """
    now = datetime.now()

    return predict_single_weather_feel(
        weather=weather,
        hour=now.hour,
        month=now.month
    )


def predict_forecast_feel(forecast: list[dict]) -> list[dict]:
    """
    Aplică modelul ML pe fiecare element din forecast.
    Returnează forecast-ul îmbogățit cu predicții ML.
    """

    enhanced_forecast = []

    for item in forecast:
        # OpenWeatherMap dă timpul în format:
        # "2026-05-04 15:00:00"
        forecast_time = datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S")

        ml_prediction = predict_single_weather_feel(
            weather=item,
            hour=forecast_time.hour,
            month=forecast_time.month
        )

        enhanced_item = {
            **item,
            "ml": ml_prediction
        }

        enhanced_forecast.append(enhanced_item)

    return enhanced_forecast