import os
import tkinter as tk
from tkinter import ttk, messagebox

from dotenv import load_dotenv

from services.aviation_weather import AviationWx
from services.openweather import OpenWeatherService

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")


#tkinter 
class WeatherGUI:

    def __init__(self, root, api_key):
        self.root = root
        #title 
        self.root.title("Weather Project")
        #set window size
        self.root.geometry("650x500")

        self.aviation_weather = AviationWx()

        if api_key:
            self.general_weather = OpenWeatherService(api_key)
        else:
            self.general_weather = None

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Python Weather Project",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # METAR input
        metar_frame = ttk.LabelFrame(
            self.root,
            text="Aviation Weather",
            padding=10
        )
        metar_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            metar_frame,
            text="Station identifier:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.station_entry = ttk.Entry(metar_frame, width=20)
        self.station_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            metar_frame,
            text="Get METAR",
            command=self.show_metar
        ).grid(row=0, column=2, padx=5, pady=5)

        # General-weather input
        weather_frame = ttk.LabelFrame(
            self.root,
            text="General Weather",
            padding=10
        )
        weather_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            weather_frame,
            text="City:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.city_entry = ttk.Entry(weather_frame, width=20)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            weather_frame,
            text="Get Weather",
            command=self.show_weather
        ).grid(row=0, column=2, padx=5, pady=5)

        # Output area
        self.output = tk.Text(
            self.root,
            width=75,
            height=18,
            wrap="word"
        )
        self.output.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Button(
            self.root,
            text="Clear",
            command=self.clear_output
        ).pack(pady=(0, 10))

    def show_metar(self):
        station_id = self.station_entry.get().strip().upper()

        if not station_id:
            messagebox.showwarning(
                "Missing identifier",
                "Please enter a station identifier."
            )
            return

        data = self.aviation_weather.get_metar(station_id)

        if not data:
            messagebox.showerror(
                "METAR unavailable",
                f"No recent METAR was found for {station_id}."
            )
            return

        metar = data[0]
        clouds = metar.get("clouds", [])

        if clouds:
            cloud_description = str(clouds[0])
        else:
            cloud_description = "No cloud layers reported"

        result = (
            f"Current METAR: {station_id}\n"
            f"--------------------------------\n"
            f"Airport: {metar.get('name', 'Unknown')}\n"
            f"Temperature: {metar.get('temp', 'N/A')} C\n"
            f"Dewpoint: {metar.get('dewp', 'N/A')} C\n"
            f"Wind direction: {metar.get('wdir', 'N/A')}\n"
            f"Wind speed: {metar.get('wspd', 'N/A')} knots\n"
            f"Visibility: {metar.get('visib', 'N/A')} SM\n"
            f"Altimeter: {metar.get('altim', 'N/A')}\n"
            f"Clouds: {cloud_description}\n"
        )

        self.display_result(result)

    def show_weather(self):
        if self.general_weather is None:
            messagebox.showerror(
                "Missing API key",
                "The OpenWeather API key is not configured."
            )
            return

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning(
                "Missing city",
                "Please enter a city."
            )
            return

        data = self.general_weather.get_weather(city)

        if not data:
            messagebox.showerror(
                "Weather unavailable",
                f"Weather could not be found for {city}."
            )
            return

        temperature_f = data["main"]["temp"]
        temperature_c = (
            self.general_weather.fahrenheit_to_celsius(temperature_f)
        )
        visibility_miles = self.general_weather.meters_to_miles(
            data.get("visibility", 0)
        )

        result = (
            f"Current Weather: {data.get('name', city)}\n"
            f"--------------------------------\n"
            f"Condition: {data['weather'][0]['description']}\n"
            f"Temperature: {temperature_f:.1f} F\n"
            f"Temperature: {temperature_c:.1f} C\n"
            f"Humidity: {data['main']['humidity']}%\n"
            f"Wind speed: {data['wind']['speed']} mph\n"
            f"Visibility: {visibility_miles:.1f} miles\n"
        )

        self.display_result(result)

    def display_result(self, result):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)

    def clear_output(self):
        self.output.delete("1.0", tk.END)




def main():
    root = tk.Tk()
    WeatherGUI(root, api_key)
    root.mainloop()


if __name__ == "__main__":
    main()
    