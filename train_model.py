import os
import random
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


MODEL_PATH = "models/weather_model.pkl"


def generate_training_data(rows=3000):
    data = []

    for _ in range(rows):
        temperature = random.uniform(-10, 40)
        humidity = random.uniform(20, 100)
        wind_speed = random.uniform(0, 18)
        clouds = random.uniform(0, 100)
        hour = random.randint(0, 23)
        month = random.randint(1, 12)

        is_day = 1 if 7 <= hour <= 20 else 0

        # Radiație solară aproximată
        if is_day:
            sun_factor = max(0, 1 - clouds / 100)
            solar_radiation = sun_factor * random.uniform(300, 900)
        else:
            solar_radiation = 0

        # Temperatură resimțită la umbră
        shadow_feels = (
            temperature
            + 0.04 * humidity
            - 0.35 * wind_speed
        )

        # Iarna vântul face temperatura să pară mai rece
        if temperature < 10:
            shadow_feels -= 0.25 * wind_speed

        # Vara umiditatea crește disconfortul
        if temperature > 25:
            shadow_feels += 0.06 * humidity

        # Temperatură resimțită la soare
        sun_feels = shadow_feels

        if is_day:
            sun_feels += solar_radiation / 180
            sun_feels += max(0, temperature - 20) * 0.08

        # Adăugăm puțin zgomot realist
        shadow_feels += random.uniform(-1.5, 1.5)
        sun_feels += random.uniform(-1.5, 1.5)

        data.append({
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "clouds": clouds,
            "hour": hour,
            "month": month,
            "is_day": is_day,
            "solar_radiation": solar_radiation,
            "shadow_feels": shadow_feels,
            "sun_feels": sun_feels,
        })

    return pd.DataFrame(data)


def train_model():
    os.makedirs("models", exist_ok=True)

    df = generate_training_data()

    features = [
        "temperature",
        "humidity",
        "wind_speed",
        "clouds",
        "hour",
        "month",
        "is_day",
        "solar_radiation",
    ]

    targets = ["shadow_feels", "sun_feels"]

    X = df[features]
    y = df[targets]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=120,
        random_state=42,
        max_depth=12
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    error = mean_absolute_error(y_test, predictions)

    joblib.dump(model, MODEL_PATH)

    print("Model antrenat cu succes.")
    print(f"Eroare medie aproximativă: {error:.2f}°C")
    print(f"Model salvat în: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()