import customtkinter as ctk
from weather_api import get_current_weather, get_forecast, WeatherAPIError


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SmartWeatherAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Weather Assistant")
        self.geometry("780x640")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Smart Weather Assistant",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=20)

        self.subtitle_label = ctk.CTkLabel(
<<<<<<< HEAD
            self,
            text="Vreme actuală + forecast pentru următoarele 24h",
            font=("Arial", 15)
=======
            self.header_frame,
            text="Vreme actuala, forecast si estimari ML pentru confort termic",
            font=("Arial", 15),
            text_color="#94a3b8",
>>>>>>> a26f391 (format)
        )
        self.subtitle_label.pack(pady=5)

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
<<<<<<< HEAD
            width=360,
            height=40,
            placeholder_text="Introdu orașul, ex: Bucharest"
=======
            height=46,
            placeholder_text="Introdu orasul, ex: Bucharest, Cluj-Napoca, London",
            font=("Arial", 15),
            corner_radius=14,
>>>>>>> a26f391 (format)
        )
        self.city_entry.grid(row=0, column=0, padx=10, pady=10)

        self.search_button = ctk.CTkButton(
            self.search_frame,
<<<<<<< HEAD
            text="Caută",
            width=120,
            height=40,
            command=self.load_weather
=======
            text="Cauta",
            height=46,
            width=130,
            corner_radius=14,
            font=("Arial", 15, "bold"),
            command=self.load_weather,
>>>>>>> a26f391 (format)
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        self.result_frame = ctk.CTkFrame(self, width=700, height=220)
        self.result_frame.pack(pady=10)
        self.result_frame.pack_propagate(False)

<<<<<<< HEAD
        self.current_weather_label = ctk.CTkLabel(
            self.result_frame,
            text="Introdu un oraș pentru a vedea vremea.",
=======
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Current weather card
        self.weather_card = self.create_card(self.content_frame, "Vreme actuala")
        self.weather_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        self.weather_label = ctk.CTkLabel(
            self.weather_card,
            text="Introdu un oras pentru a vedea vremea.",
>>>>>>> a26f391 (format)
            font=("Arial", 16),
            justify="left"
        )
        self.current_weather_label.pack(padx=20, pady=20, anchor="w")

<<<<<<< HEAD
        self.forecast_title = ctk.CTkLabel(
            self,
            text="Forecast următoarele 24h",
            font=("Arial", 20, "bold")
        )
        self.forecast_title.pack(pady=10)

        self.forecast_box = ctk.CTkTextbox(
            self,
            width=700,
            height=220,
            font=("Consolas", 13)
=======
        # ML card
        self.ml_card = self.create_card(self.content_frame, "Estimari ML")
        self.ml_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        self.ml_label = ctk.CTkLabel(
            self.ml_card,
            text="Estimarile ML vor aparea dupa cautare.",
            font=("Arial", 16),
            justify="left",
            anchor="w",
            text_color="#e2e8f0",
>>>>>>> a26f391 (format)
        )
        self.forecast_box.pack(pady=5)

<<<<<<< HEAD
        self.forecast_box.insert("end", "Forecast-ul va apărea aici.")
        self.forecast_box.configure(state="disabled")
=======
        # Recommendation card
        self.recommendation_card = self.create_card(
            self.content_frame, "Recomandare inteligenta"
        )
        self.recommendation_card.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=10
        )

        self.recommendation_label = ctk.CTkLabel(
            self.recommendation_card,
            text="Recomandarea va aparea aici.",
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
            self.content_frame, "Forecast urmatoarele 24h"
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
            text="Cum ti s-a parut temperatura fata de predictia ML?",
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
            text="Mi s-a parut mai rece",
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
            text="Mi s-a parut mai cald",
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
>>>>>>> a26f391 (format)

    def load_weather(self):
        # Citim orasul introdus de utilizator.
        city = self.city_entry.get().strip()

        if not city:
            self.show_error("Te rog introdu un oras.")
            return

        self.search_button.configure(state="disabled", text="Se încarcă...")
        self.update_idletasks()

        try:
            current = get_current_weather(city)
            forecast = get_forecast(city)

            self.display_current_weather(current)
            self.display_forecast(forecast)

        except WeatherAPIError as error:
            self.show_error(str(error))
        except Exception as error:
            self.show_error(f"A aparut o eroare: {error}")
        finally:
<<<<<<< HEAD
            self.search_button.configure(state="normal", text="Caută")
=======
            self.set_loading(False)

    def set_loading(self, is_loading: bool):
        if is_loading:
            self.search_button.configure(state="disabled", text="Se încarca...")
            self.status_label.configure(
                text="Se cauta datele meteo...", text_color="#facc15"
            )
        else:
            self.search_button.configure(state="normal", text="Cauta")
>>>>>>> a26f391 (format)

    def display_current_weather(self, weather: dict):
        text = (
            f"{weather['city']}, {weather['country']}\n\n"
<<<<<<< HEAD
            f"Condiții: {weather['description']}\n"
            f"Temperatură: {weather['temperature']}°C\n"
            f"Se simte ca: {weather['feels_like']}°C\n"
=======
            f"Conditii: {weather['description']}\n"
<<<<<<< HEAD
            f"Temperatura API: {weather['temperature']}°C\n"
            f"Se simte ca API: {weather['feels_like']}°C\n\n"
>>>>>>> a26f391 (format)
=======
            f"Temperatura: {weather['temperature']}°C\n"
            f"Se simte ca: {weather['feels_like']}°C\n\n"
>>>>>>> 9c59c84 (gui text fix)
            f"Umiditate: {weather['humidity']}%\n"
            f"Presiune: {weather['pressure']} hPa\n"
            f"Vant: {weather['wind_speed']} m/s\n"
            f"Nebulozitate: {weather['clouds']}%"
        )

<<<<<<< HEAD
        self.current_weather_label.configure(text=text)
=======
        self.weather_label.configure(text=text)

    def display_ml_prediction(self, ml_prediction: dict):
        text = (
            f"Se simte la umbra: {ml_prediction['shadow_feels']}°C\n"
            f"Se simte la soare: {ml_prediction['sun_feels']}°C\n"
            f"Scor confort: {ml_prediction['comfort_score']}/100\n"
            f"Radiatie solara estimata: {ml_prediction['solar_radiation']} W/m²"
        )

        self.ml_label.configure(text=text)

    def display_recommendation(self, ml_prediction: dict):
        self.recommendation_label.configure(text=ml_prediction["recommendation"])
>>>>>>> a26f391 (format)

    def display_forecast(self, forecast: list[dict]):
        self.forecast_box.configure(state="normal")
        self.forecast_box.delete("1.0", "end")

        for item in forecast:
            line = (
                f"{item['time']} | "
                f"{item['temperature']}°C | "
                f"Feels: {item['feels_like']}°C | "
                f"Vânt: {item['wind_speed']} m/s | "
                f"{item['description']}\n"
            )
            self.forecast_box.insert("end", line)

<<<<<<< HEAD
        self.forecast_box.configure(state="disabled")

    def show_error(self, message: str):
        self.current_weather_label.configure(text=f"Eroare: {message}")
=======
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
                text=f"Umbra: {ml['shadow_feels']}°C",
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
                text=f"{item['description']} | Vant: {item['wind_speed']} m/s | Umiditate: {item['humidity']}%",
                font=("Arial", 13),
                text_color="#94a3b8",
            )
            desc_label.grid(
                row=1, column=0, columnspan=5, sticky="w", padx=14, pady=(0, 12)
            )

    def submit_feedback(self, feedback_type: str):
        if self.current_weather_data is None or self.current_ml_prediction is None:
            self.status_label.configure(
                text="Cauta mai întai vremea pentru un oras.", text_color="#facc15"
            )
            return

        try:
            save_feedback(
                weather=self.current_weather_data,
                ml_prediction=self.current_ml_prediction,
                feedback_type=feedback_type,
            )

            feedback_text = {
                "colder": "Feedback salvat: ti s-a parut mai rece.",
                "correct": "Feedback salvat: predictia a fost corecta.",
                "warmer": "Feedback salvat: ti s-a parut mai cald.",
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
        self.weather_label.configure(text="Nu s-au putut încarca datele.")
        self.ml_label.configure(text="Estimarile ML nu sunt disponibile.")
        self.recommendation_label.configure(text=message)
>>>>>>> a26f391 (format)

        self.forecast_box.configure(state="normal")
        self.forecast_box.delete("1.0", "end")
        self.forecast_box.insert("end", "Nu există forecast disponibil.")
        self.forecast_box.configure(state="disabled")


if __name__ == "__main__":
    app = SmartWeatherAssistant()
    app.mainloop()