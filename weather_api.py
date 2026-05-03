import requests
from config import API_KEY, BASE_CURRENT_URL, BASE_FORECAST_URL

class WeatherAPIError(Exception):
    pass


def get_current_weather(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ro",
    }

    response = requests.get(BASE_CURRENT_URL, params=params, timeout=10)

    if response.status_code != 200:
        try:
            message = response.json().get("message", "Eroare necunoscută")
        except ValueError:
            message = "Eroare necunoscută"

        raise WeatherAPIError(f"Nu am putut lua vremea actuală: {message}")

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