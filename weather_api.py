import requests
from config import API_KEY, BASE_CURRENT_URL, BASE_FORECAST_URL


class WeatherAPIError(Exception):
    pass


def get_current_weather(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en",
    }

    response = requests.get(BASE_CURRENT_URL, params=params, timeout=10)

    if response.status_code != 200:
        try:
            message = response.json().get("message", "Eroare necunoscuta")
        except ValueError:
            message = "Eroare necunoscuta"

        raise WeatherAPIError(f"Nu am putut lua vremea actuala: {message}")

    data = response.json()

    return {
        "city": data.get("name", city),
        "country": data.get("sys", {}).get("country", ""),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "description": data["weather"][0]["description"].capitalize(),
    }


def get_forecast(city: str, limit: int = 8) -> list[dict]:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ro",
    }

    response = requests.get(BASE_FORECAST_URL, params=params, timeout=10)

    if response.status_code != 200:
        try:
            message = response.json().get("message", "Eroare necunoscuta")
        except ValueError:
            message = "Eroare necunoscuta"

        raise WeatherAPIError(f"Nu am putut lua forecast-ul: {message}")

    data = response.json()
    forecast_items = data.get("list", [])[:limit]

    forecast = []

    for item in forecast_items:
        forecast.append({
            "time": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"],
            "clouds": item["clouds"]["all"],
            "description": item["weather"][0]["description"].capitalize(),
        })

    return forecast