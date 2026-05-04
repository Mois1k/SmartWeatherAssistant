import os
import shutil
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from train_model import generate_training_data


FEEDBACK_FILE = "data/user_feedback.csv"

MODEL_PATH = "models/weather_model.pkl"
BACKUP_MODEL_PATH = "models/weather_model_base_backup.pkl"


FEATURES = [
    "temperature",
    "humidity",
    "wind_speed",
    "clouds",
    "hour",
    "month",
    "is_day",
    "solar_radiation",
]

TARGETS = [
    "shadow_feels",
    "sun_feels",
]


def feedback_to_delta(feedback_type: str) -> tuple[float, float]:
    """
    Transforma feedback-ul utilizatorului în ajustari pentru target.

    colder  -> modelul a prezis prea cald, deci scadem predictia
    correct -> pastram predictia
    warmer  -> modelul a prezis prea rece, deci crestem predictia
    """

    if feedback_type == "colder":
        return -1.5, -2.0

    if feedback_type == "warmer":
        return 1.5, 2.0

    return 0.0, 0.0


def load_feedback_data() -> pd.DataFrame:
    if not os.path.exists(FEEDBACK_FILE):
        raise FileNotFoundError(
            f"Nu exista {FEEDBACK_FILE}. Salveaza mai întai feedback din aplicatie."
        )

    df = pd.read_csv(FEEDBACK_FILE)

    if df.empty:
        raise ValueError("Fisierul de feedback exista, dar este gol.")

    return df


def build_personalized_dataset(feedback_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for _, row in feedback_df.iterrows():
        timestamp = pd.to_datetime(row["timestamp"])

        hour = timestamp.hour
        month = timestamp.month
        is_day = 1 if 7 <= hour <= 20 else 0

        shadow_delta, sun_delta = feedback_to_delta(row["feedback_type"])

        personalized_shadow = float(row["ml_shadow_feels"]) + shadow_delta
        personalized_sun = float(row["ml_sun_feels"]) + sun_delta

        rows.append({
            "temperature": float(row["temperature"]),
            "humidity": float(row["humidity"]),
            "wind_speed": float(row["wind_speed"]),
            "clouds": float(row["clouds"]),
            "hour": hour,
            "month": month,
            "is_day": is_day,
            "solar_radiation": float(row["solar_radiation"]),
            "shadow_feels": personalized_shadow,
            "sun_feels": personalized_sun,
        })

    personalized_df = pd.DataFrame(rows)

    return personalized_df


def retrain_model():
    os.makedirs("models", exist_ok=True)

    feedback_df = load_feedback_data()
    personalized_df = build_personalized_dataset(feedback_df)

    print(f"Feedback-uri gasite: {len(personalized_df)}")

    synthetic_df = generate_training_data(rows=3000)

    # Repetam datele personale ca sa aiba greutate mai mare în model.
    # Daca ai putine feedback-uri, altfel ar fi ignorate de datele sintetice.
    personalized_weighted_df = pd.concat(
        [personalized_df] * 25,
        ignore_index=True
    )

    final_df = pd.concat(
        [synthetic_df, personalized_weighted_df],
        ignore_index=True
    )

    X = final_df[FEATURES]
    y = final_df[TARGETS]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        max_depth=14
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    error = mean_absolute_error(y_test, predictions)

    if os.path.exists(MODEL_PATH) and not os.path.exists(BACKUP_MODEL_PATH):
        shutil.copy(MODEL_PATH, BACKUP_MODEL_PATH)
        print(f"Backup creat: {BACKUP_MODEL_PATH}")

    joblib.dump(model, MODEL_PATH)

    print("Model reantrenat cu succes.")
    print(f"Eroare medie aproximativa: {error:.2f}°C")
    print(f"Model personalizat salvat în: {MODEL_PATH}")


if __name__ == "__main__":
    try:
        retrain_model()
    except Exception as error:
        print(f"Eroare la reantrenare: {error}")