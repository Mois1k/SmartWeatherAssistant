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
            self,
            text="Vreme actuală + forecast pentru următoarele 24h",
            font=("Arial", 15)
        )
        self.subtitle_label.pack(pady=5)

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            width=360,
            height=40,
            placeholder_text="Introdu orașul, ex: Bucharest"
        )
        self.city_entry.grid(row=0, column=0, padx=10, pady=10)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Caută",
            width=120,
            height=40,
            command=self.load_weather
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        self.result_frame = ctk.CTkFrame(self, width=700, height=220)
        self.result_frame.pack(pady=10)
        self.result_frame.pack_propagate(False)

        self.current_weather_label = ctk.CTkLabel(
            self.result_frame,
            text="Introdu un oraș pentru a vedea vremea.",
            font=("Arial", 16),
            justify="left"
        )
        self.current_weather_label.pack(padx=20, pady=20, anchor="w")

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
        )
        self.forecast_box.pack(pady=5)

        self.forecast_box.insert("end", "Forecast-ul va apărea aici.")
        self.forecast_box.configure(state="disabled")

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
            self.search_button.configure(state="normal", text="Caută")

    def display_current_weather(self, weather: dict):
        text = (
            f"{weather['city']}, {weather['country']}\n\n"

            f"Condiții: {weather['description']}\n"
            f"Temperatură: {weather['temperature']}°C\n"
            f"Se simte ca: {weather['feels_like']}°C\n"

            f"Conditii: {weather['description']}\n"

            f"Temperatura API: {weather['temperature']}°C\n"
            f"Se simte ca API: {weather['feels_like']}°C\n\n"

            f"Temperatura: {weather['temperature']}°C\n"
            f"Se simte ca: {weather['feels_like']}°C\n\n"
            f"Umiditate: {weather['humidity']}%\n"
            f"Presiune: {weather['pressure']} hPa\n"
            f"Vant: {weather['wind_speed']} m/s\n"
            f"Nebulozitate: {weather['clouds']}%"
        )

        self.current_weather_label.configure(text=text)

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

        self.forecast_box.configure(state="disabled")

    def show_error(self, message: str):
        self.current_weather_label.configure(text=f"Eroare: {message}")

        self.forecast_box.configure(state="normal")
        self.forecast_box.delete("1.0", "end")
        self.forecast_box.insert("end", "Nu există forecast disponibil.")
        self.forecast_box.configure(state="disabled")


if __name__ == "__main__":
    app = SmartWeatherAssistant()
    app.mainloop()