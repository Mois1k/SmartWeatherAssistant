# Smart Weather Assistant

Smart Weather Assistant este o aplicatie Python cu interfata grafica moderna care afiseaza vremea actuala, forecast-ul pe urmatoarele ore si estimari bazate pe Machine Learning pentru temperatura resimtita la umbra si la soare.

## Descriere scurta

Asistent meteo cu GUI, API si predictii ML personalizate.

## Functionalitati

- Cautare meteo dupa oras
- Integrare cu OpenWeatherMap API
- Afisare vreme actuala:
  - temperatura
  - temperatura resimtita API
  - umiditate
  - presiune
  - vant
  - nebulozitate
  - conditii meteo
- Forecast pentru urmatoarele 24 de ore
- Estimari ML pentru:
  - temperatura resimtita la umbra
  - temperatura resimtita la soare
  - scor de confort termic
  - radiatie solara estimata
- Recomandari inteligente in functie de conditiile meteo
- Interfata grafica moderna cu CustomTkinter
- Sistem de feedback personalizat
- Reantrenarea modelului pe baza feedback-ului utilizatorului

## Tehnologii folosite

- Python 3
- CustomTkinter
- Requests
- Pandas
- Scikit-learn
- Joblib
- OpenWeatherMap API

## Structura proiectului

```text
WeatherApp/
│
├── main.py                  # Interfata grafica a aplicatiei
├── weather_api.py           # Comunicarea cu OpenWeatherMap API
├── ml_model.py              # Predictii ML pentru vreme actuala si forecast
├── train_model.py           # Antrenarea modelului initial
├── retrain_model.py         # Reantrenarea modelului cu feedback personal
├── feedback_manager.py      # Salvarea feedback-ului utilizatorului
├── config.py                # Cheia API si endpoint-urile
├── requirements.txt         # Dependentele proiectului
├── README.md
│
├── models/
│   ├── weather_model.pkl
│   └── weather_model_base_backup.pkl
│
└── data/
    └── user_feedback.csv
```

## Instalare

### 1. Cloneaza repository-ul

```bash
git clone https://github.com/Mois1k/SmartWeatherAssistant.git
cd SmartWeatherApp
```

### 2. Instaleaza dependentele

Pe WSL / Ubuntu, system-wide:

```bash
sudo apt update
sudo apt install python3-pip python3-tk python3-requests python3-pandas python3-sklearn python3-joblib
sudo python3 -m pip install customtkinter --break-system-packages
```

Alternativ, cu `requirements.txt`:

```bash
sudo python3 -m pip install -r requirements.txt --break-system-packages
```

## Configurare API

Aplicatia foloseste OpenWeatherMap API.

Creeaza un fisier `config.py` in radacina proiectului:

```python
API_KEY = "CHEIA_TA_OPENWEATHERMAP"

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
```
## Antrenarea modelului ML

inainte de prima rulare completa, antreneaza modelul:

```bash
python3 train_model.py
```

Modelul va fi salvat in:

```text
models/weather_model.pkl
```

Exemplu rezultat:

```text
Model antrenat cu succes.
Eroare medie aproximativa: 0.96°C
Model salvat in: models/weather_model.pkl
```

## Rularea aplicatiei

```bash
python3 main.py
```

Apoi introdu un oras, de exemplu:

```text
Bucharest
Cluj-Napoca
London
Paris
```

## Feedback personalizat

Dupa ce aplicatia afiseaza predictiile ML, utilizatorul poate oferi feedback:

- Mi s-a parut mai rece
- A fost corect
- Mi s-a parut mai cald

Feedback-ul este salvat in:

```text
data/user_feedback.csv
```

Acest feedback este folosit ulterior pentru personalizarea modelului.

## Reantrenarea modelului

Dupa ce ai strans mai multe feedback-uri, ruleaza:

```bash
python3 retrain_model.py
```

Scriptul va:

- citi feedback-ul din `data/user_feedback.csv`
- ajusta datele de antrenare
- crea backup pentru modelul vechi
- salva modelul personalizat in `models/weather_model.pkl`

Dupa reantrenare, aplicatia va folosi automat modelul nou.

## Cum functioneaza Machine Learning-ul

Modelul foloseste `RandomForestRegressor` pentru a estima doua valori:

```text
shadow_feels
sun_feels
```

Adica:

- temperatura resimtita la umbra
- temperatura resimtita la soare

Datele de intrare sunt:

```text
temperature
humidity
wind_speed
clouds
hour
month
is_day
solar_radiation
```

Modelul este initial antrenat pe date generate artificial, apoi poate fi personalizat cu feedback-ul utilizatorului.

## Nota despre personalizare

Predictiile ML devin mai personalizate pe masura ce utilizatorul ofera mai mult feedback. Pentru rezultate mai vizibile, este recomandat sa colectezi cel putin 10–20 feedback-uri inainte de reantrenare.

## Posibile imbunatatiri viitoare

- Grafic pentru forecast:
  - temperatura API
  - temperatura ML la umbra
  - temperatura ML la soare
  - scor confort
- Salvarea istoricului cautarilor
- Selectarea unitatii de masura
- Mod light/dark
- Export feedback in CSV
- Dashboard cu statistici
- Integrare cu un API pentru radiatie solara reala
- Recomandari pentru activitati:
  - alergat
  - mers pe jos
  - bicicleta
  - condus
- Packaging ca aplicatie desktop
