# Smart Weather Assistant

Smart Weather Assistant este o aplicație Python cu interfață grafică modernă care afișează vremea actuală, forecast-ul pe următoarele ore și estimări bazate pe Machine Learning pentru temperatura resimțită la umbră și la soare.

## Descriere scurtă

Asistent meteo cu GUI, API și predicții ML personalizate.

## Funcționalități

- Căutare meteo după oraș
- Integrare cu OpenWeatherMap API
- Afișare vreme actuală:
  - temperatură
  - temperatură resimțită API
  - umiditate
  - presiune
  - vânt
  - nebulozitate
  - condiții meteo
- Forecast pentru următoarele 24 de ore
- Estimări ML pentru:
  - temperatura resimțită la umbră
  - temperatura resimțită la soare
  - scor de confort termic
  - radiație solară estimată
- Recomandări inteligente în funcție de condițiile meteo
- Interfață grafică modernă cu CustomTkinter
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
├── main.py                  # Interfața grafică a aplicației
├── weather_api.py           # Comunicarea cu OpenWeatherMap API
├── ml_model.py              # Predicții ML pentru vreme actuală și forecast
├── train_model.py           # Antrenarea modelului inițial
├── retrain_model.py         # Reantrenarea modelului cu feedback personal
├── feedback_manager.py      # Salvarea feedback-ului utilizatorului
├── config.py                # Cheia API și endpoint-urile
├── requirements.txt         # Dependențele proiectului
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

### 1. Clonează repository-ul

```bash
git clone https://github.com/USERNAME/WeatherApp.git
cd WeatherApp
```

Înlocuiește `USERNAME` cu numele tău de utilizator GitHub.

### 2. Instalează dependențele

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

Aplicația folosește OpenWeatherMap API.

Creează un fișier `config.py` în rădăcina proiectului:

```python
API_KEY = "CHEIA_TA_OPENWEATHERMAP"

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
```

Nu urca `config.py` pe GitHub, deoarece conține cheia ta API.

Recomandat: creează și un fișier `config.example.py`:

```python
API_KEY = "PUNE_CHEIA_TA_AICI"

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
```

## Antrenarea modelului ML

Înainte de prima rulare completă, antrenează modelul:

```bash
python3 train_model.py
```

Modelul va fi salvat în:

```text
models/weather_model.pkl
```

Exemplu rezultat:

```text
Model antrenat cu succes.
Eroare medie aproximativă: 0.96°C
Model salvat în: models/weather_model.pkl
```

## Rularea aplicației

```bash
python3 main.py
```

Apoi introdu un oraș, de exemplu:

```text
Bucharest
Cluj-Napoca
London
Paris
```

## Feedback personalizat

După ce aplicația afișează predicțiile ML, utilizatorul poate oferi feedback:

- Mi s-a părut mai rece
- A fost corect
- Mi s-a părut mai cald

Feedback-ul este salvat în:

```text
data/user_feedback.csv
```

Acest feedback este folosit ulterior pentru personalizarea modelului.

## Reantrenarea modelului

După ce ai strâns mai multe feedback-uri, rulează:

```bash
python3 retrain_model.py
```

Scriptul va:

- citi feedback-ul din `data/user_feedback.csv`
- ajusta datele de antrenare
- crea backup pentru modelul vechi
- salva modelul personalizat în `models/weather_model.pkl`

După reantrenare, aplicația va folosi automat modelul nou.

## Cum funcționează Machine Learning-ul

Modelul folosește `RandomForestRegressor` pentru a estima două valori:

```text
shadow_feels
sun_feels
```

Adică:

- temperatura resimțită la umbră
- temperatura resimțită la soare

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

Modelul este inițial antrenat pe date generate artificial, apoi poate fi personalizat cu feedback-ul utilizatorului.

## Notă despre personalizare

Predicțiile ML devin mai personalizate pe măsură ce utilizatorul oferă mai mult feedback. Pentru rezultate mai vizibile, este recomandat să colectezi cel puțin 10–20 feedback-uri înainte de reantrenare.

## Fișiere care nu ar trebui urcate pe GitHub

Adaugă în `.gitignore`:

```gitignore
__pycache__/
*.pyc
.venv/
.env
config.py
data/
models/
```

Dacă vrei să păstrezi structura folderelor `data` și `models`, poți folosi `.gitkeep`:

```bash
touch data/.gitkeep
touch models/.gitkeep
```

și în `.gitignore`:

```gitignore
data/*
!data/.gitkeep

models/*
!models/.gitkeep
```

## Posibile îmbunătățiri viitoare

- Grafic pentru forecast:
  - temperatură API
  - temperatură ML la umbră
  - temperatură ML la soare
  - scor confort
- Salvarea istoricului căutărilor
- Selectarea unității de măsură
- Mod light/dark
- Export feedback în CSV
- Dashboard cu statistici
- Integrare cu un API pentru radiație solară reală
- Recomandări pentru activități:
  - alergat
  - mers pe jos
  - bicicletă
  - condus
- Packaging ca aplicație desktop

## Autor

Proiect realizat ca aplicație Python practică folosind API, GUI și Machine Learning.
