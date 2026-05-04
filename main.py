import customtkinter as ctk
from weather_api import get_current_weather, get_forecast, WeatherAPIError
from ml import predict_weather_feel, predict_forecast_feel, MLModelError
from feedback_manager import save_feedback

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SmartWeatherAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Weather Assistant")
        self.geometry("980x720")
        self.minsize(820, 600)
        self.current_weather_data = None
        self.current_ml_prediction = None

        self.configure(fg_color="#0f172a")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Smart Weather Assistant",
            font=("Arial", 32, "bold"),
            text_color="#f8fafc",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Vreme actuală, forecast și estimări ML pentru confort termic",
            font=("Arial", 15),
            text_color="#94a3b8",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        # Search area
        self.search_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e293b")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=12)
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            height=46,
            placeholder_text="Introdu orașul, ex: Bucharest, Cluj-Napoca, London",
            font=("Arial", 15),
            corner_radius=14,
        )
        self.city_entry.grid(row=0, column=0, sticky="ew", padx=(18, 10), pady=18)
        self.city_entry.bind("<Return>", lambda event: self.load_weather())

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Caută",
            height=46,
            width=130,
            corner_radius=14,
            font=("Arial", 15, "bold"),
            command=self.load_weather,
        )
        self.search_button.grid(row=0, column=1, sticky="e", padx=(0, 18), pady=18)

        # Main content
        self.content_frame = ctk.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Current weather card
        self.weather_card = self.create_card(self.content_frame, "Vreme actuală")
        self.weather_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        self.weather_label = ctk.CTkLabel(
            self.weather_card,
            text="Introdu un oraș pentru a vedea vremea.",
            font=("Arial", 16),
            justify="left",
            anchor="w",
            text_color="#e2e8f0",
        )
        self.weather_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 18))

        # ML card
        self.ml_card = self.create_card(self.content_frame, "Estimări ML")
        self.ml_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        self.ml_label = ctk.CTkLabel(
            self.ml_card,
            text="Estimările ML vor apărea după căutare.",
            font=("Arial", 16),
            justify="left",
            anchor="w",
            text_color="#e2e8f0",
        )
        self.ml_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 18))

        # Recommendation card
        self.recommendation_card = self.create_card(
            self.content_frame, "Recomandare inteligentă"
        )
        self.recommendation_card.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=10
        )

        self.recommendation_label = ctk.CTkLabel(
            self.recommendation_card,
            text="Recomandarea va apărea aici.",
            font=("Arial", 17),
            wraplength=850,
            justify="left",
            anchor="w",
            text_color="#f8fafc",
        )
        self.recommendation_label.grid(
            row=1, column=0, sticky="ew", padx=18, pady=(4, 18)
        )

        # Forecast card
        self.forecast_card = self.create_card(
            self.content_frame, "Forecast următoarele 24h"
        )
        self.forecast_card.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        self.forecast_list_frame = ctk.CTkFrame(
            self.forecast_card, fg_color="transparent"
        )
        self.forecast_list_frame.grid(
            row=1, column=0, sticky="ew", padx=18, pady=(4, 18)
        )
        self.forecast_list_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self, text="Ready", font=("Arial", 13), text_color="#94a3b8"
        )
        self.status_label.grid(row=3, column=0, sticky="w", padx=26, pady=(0, 10))
        # Feedback card
        self.feedback_card = self.create_card(
            self.content_frame, "Feedback personalizat"
        )
        self.feedback_card.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        self.feedback_label = ctk.CTkLabel(
            self.feedback_card,
            text="Cum ți s-a părut temperatura față de predicția ML?",
            font=("Arial", 15),
            text_color="#cbd5e1",
        )
        self.feedback_label.grid(row=1, column=0, sticky="w", padx=18, pady=(4, 10))

        self.feedback_buttons_frame = ctk.CTkFrame(
            self.feedback_card, fg_color="transparent"
        )
        self.feedback_buttons_frame.grid(
            row=2, column=0, sticky="ew", padx=18, pady=(0, 18)
        )
        self.feedback_buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.colder_button = ctk.CTkButton(
            self.feedback_buttons_frame,
            text="Mi s-a părut mai rece",
            height=38,
            corner_radius=12,
            command=lambda: self.submit_feedback("colder"),
        )
        self.colder_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.correct_button = ctk.CTkButton(
            self.feedback_buttons_frame,
            text="A fost corect",
            height=38,
            corner_radius=12,
            command=lambda: self.submit_feedback("correct"),
        )
        self.correct_button.grid(row=0, column=1, sticky="ew", padx=8)

        self.warmer_button = ctk.CTkButton(
            self.feedback_buttons_frame,
            text="Mi s-a părut mai cald",
            height=38,
            corner_radius=12,
            command=lambda: self.submit_feedback("warmer"),
        )
        self.warmer_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

    def create_card(self, parent, title: str):
        card = ctk.CTkFrame(parent, corner_radius=22, fg_color="#1e293b")
        card.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            card, text=title, font=("Arial", 19, "bold"), text_color="#f8fafc"
        )
        title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(18, 8))

        return card

    def load_weather(self):
        city = self.city_entry.get().strip()

        if not city:
            self.show_error("Te rog introdu un oraș.")
            return

        self.set_loading(True)

        try:
            current = get_current_weather(city)
            forecast = get_forecast(city)

            ml_prediction = predict_weather_feel(current)
            enhanced_forecast = predict_forecast_feel(forecast)
            self.current_weather_data = current
            self.current_ml_prediction = ml_prediction

            self.display_current_weather(current)
            self.display_ml_prediction(ml_prediction)
            self.display_recommendation(ml_prediction)
            self.display_forecast(enhanced_forecast)

            self.status_label.configure(
                text=f"Date actualizate pentru {current['city']}, {current['country']}",
                text_color="#22c55e",
            )

        except WeatherAPIError as error:
            self.show_error(str(error))
        except MLModelError as error:
            self.show_error(str(error))
        except Exception as error:
            self.show_error(f"A apărut o eroare: {error}")
        finally:
            self.set_loading(False)

    def set_loading(self, is_loading: bool):
        if is_loading:
            self.search_button.configure(state="disabled", text="Se încarcă...")
            self.status_label.configure(
                text="Se caută datele meteo...", text_color="#facc15"
            )
        else:
            self.search_button.configure(state="normal", text="Caută")

        self.update_idletasks()

    def display_current_weather(self, weather: dict):
        text = (
            f"{weather['city']}, {weather['country']}\n\n"
            f"Condiții: {weather['description']}\n"
            f"Temperatură API: {weather['temperature']}°C\n"
            f"Se simte ca API: {weather['feels_like']}°C\n\n"
            f"Umiditate: {weather['humidity']}%\n"
            f"Presiune: {weather['pressure']} hPa\n"
            f"Vânt: {weather['wind_speed']} m/s\n"
            f"Nebulozitate: {weather['clouds']}%"
        )

        self.weather_label.configure(text=text)

    def display_ml_prediction(self, ml_prediction: dict):
        text = (
            f"Se simte la umbră: {ml_prediction['shadow_feels']}°C\n"
            f"Se simte la soare: {ml_prediction['sun_feels']}°C\n"
            f"Scor confort: {ml_prediction['comfort_score']}/100\n"
            f"Radiație solară estimată: {ml_prediction['solar_radiation']} W/m²"
        )

        self.ml_label.configure(text=text)

    def display_recommendation(self, ml_prediction: dict):
        self.recommendation_label.configure(text=ml_prediction["recommendation"])

    def display_forecast(self, forecast: list[dict]):
        for widget in self.forecast_list_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(forecast):
            ml = item["ml"]

            row = ctk.CTkFrame(
                self.forecast_list_frame, corner_radius=16, fg_color="#334155"
            )
            row.grid(row=index, column=0, sticky="ew", pady=6)
            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(1, weight=1)
            row.grid_columnconfigure(2, weight=1)
            row.grid_columnconfigure(3, weight=1)
            row.grid_columnconfigure(4, weight=1)

            time_label = ctk.CTkLabel(
                row, text=item["time"], font=("Arial", 14, "bold"), text_color="#f8fafc"
            )
            time_label.grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

            temp_label = ctk.CTkLabel(
                row,
                text=f"API: {item['temperature']}°C",
                font=("Arial", 14),
                text_color="#e2e8f0",
            )
            temp_label.grid(row=0, column=1, sticky="w", padx=14, pady=(12, 4))

            shadow_label = ctk.CTkLabel(
                row,
                text=f"Umbră: {ml['shadow_feels']}°C",
                font=("Arial", 14),
                text_color="#cbd5e1",
            )
            shadow_label.grid(row=0, column=2, sticky="w", padx=14, pady=(12, 4))

            sun_label = ctk.CTkLabel(
                row,
                text=f"Soare: {ml['sun_feels']}°C",
                font=("Arial", 14),
                text_color="#cbd5e1",
            )
            sun_label.grid(row=0, column=3, sticky="w", padx=14, pady=(12, 4))

            score_label = ctk.CTkLabel(
                row,
                text=f"Confort: {ml['comfort_score']}/100",
                font=("Arial", 14, "bold"),
                text_color="#facc15",
            )
            score_label.grid(row=0, column=4, sticky="e", padx=14, pady=(12, 4))

            desc_label = ctk.CTkLabel(
                row,
                text=f"{item['description']} | Vânt: {item['wind_speed']} m/s | Umiditate: {item['humidity']}%",
                font=("Arial", 13),
                text_color="#94a3b8",
            )
            desc_label.grid(
                row=1, column=0, columnspan=5, sticky="w", padx=14, pady=(0, 12)
            )

    def submit_feedback(self, feedback_type: str):
        if self.current_weather_data is None or self.current_ml_prediction is None:
            self.status_label.configure(
                text="Caută mai întâi vremea pentru un oraș.", text_color="#facc15"
            )
            return

        try:
            save_feedback(
                weather=self.current_weather_data,
                ml_prediction=self.current_ml_prediction,
                feedback_type=feedback_type,
            )

            feedback_text = {
                "colder": "Feedback salvat: ți s-a părut mai rece.",
                "correct": "Feedback salvat: predicția a fost corectă.",
                "warmer": "Feedback salvat: ți s-a părut mai cald.",
            }

            self.status_label.configure(
                text=feedback_text.get(feedback_type, "Feedback salvat."),
                text_color="#22c55e",
            )

        except Exception as error:
            self.status_label.configure(
                text=f"Nu am putut salva feedback-ul: {error}", text_color="#ef4444"
            )

    def show_error(self, message: str):
        self.weather_label.configure(text="Nu s-au putut încărca datele.")
        self.ml_label.configure(text="Estimările ML nu sunt disponibile.")
        self.recommendation_label.configure(text=message)

        for widget in self.forecast_list_frame.winfo_children():
            widget.destroy()

        self.status_label.configure(text=f"Eroare: {message}", text_color="#ef4444")


if __name__ == "__main__":
    app = SmartWeatherAssistant()
    app.mainloop()
