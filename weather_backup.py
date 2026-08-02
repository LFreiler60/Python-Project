import requests
import os
import tkinter as tk
from tkinter import ttk, messagebox

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")


class AviationWx:

    #init to store url incase add other functions such as taf or pireps
    def __init__(self):
        self.metar_url = "https://aviationweather.gov/api/data/metar"


    
    def get_metar(self, station_id):
        parameters = {
            "ids" : station_id,
             "format" : "json"
            }

        try:    #requests.get(url, params)
            metar_data = requests.get(
                self.metar_url,
                params = parameters
                timeout=15,
              )

              #status code 200 = success
            if metar_data.status_code == 200:
                return metar_data.json()
             #city not found
            elif metar_data.status_code == 404:   
                print ("ICAO not found.")
                return None
            else:
                print("An unexpected error occured.")
                return None
                
            #weather server was not reached 
        except requests.exceptions.RequestException:
            print("Unable to connect to the weather service.")
            return None
    
    def display_metar(self, data):
        if not data:
            print("Unable to display Metar")
            return
        
        # data is a dict in a LIST, must provide indexing to access dict
        metar = data[0]
        #accessing dictionary values
        airport = metar["name"]
        temp = metar["temp"]
        dewpoint = metar["dewp"]
        wind_dir = metar["wdir"]
        wind_speed = metar["wspd"]
        visibility = metar["visib"]
        altimeter_setting = metar["altim"]
        elevation = metar["elev"]
        
        #go to metar dictionary and get value in clouds key
        #clouds is now cloud list
        #if sky is clear code will fail without else 
        clouds = metar.get("clouds", [])
        if clouds:
            first_cloud = clouds[0]
        else:
            first_cloud = "No cloud layers reported"

        print("Current Metar")
        print("------------------------")
        print(f"Airport: {airport}")
        print(f"Temp: {temp} C")
        print(f"Cloud layers: {first_cloud}")
        print(f"Dewpoint: {dewpoint}")
        print(f"Wind Direction: {wind_dir}")
        print(f"Wind Speed: {wind_speed} knots")
        print(f"Visibilty: {visibility} SM")
        print(f"Alitmeter Setting: {altimeter_setting}")
        print(f"Elevation: {elevation} MSL")



    def run_metar(self):

        station_id = input("Please enter station identifier: ").strip().upper()

        if not station_id:
            print("Please enter an identifer:")
            return

        if station_id == "":
            print("Please enter identifier: ")
            return
        
        data = self.get_metar(station_id)

        if data is None:
            print("Identifier not found")
            return
        
        self.display_metar(data)




class WeatherApp:
    #check for API here since aviationwx doesnt requier API key
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("WeatherApp requires an OpenWeather API key")

        self.api_key = api_key
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        # dicitonary, parameters sent to OpenWeather 
        parameters = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }

        #try block to test if weather server was reached
        try:   
            response = requests.get(
                self.weather_url,
                params=parameters
                timeout=15,
            )

            #status code 200 = success
            if response.status_code == 200:
                return response.json()
            #city not found
            elif response.status_code == 404:   
                print ("City not found.")
                return None
            else:
                print("An unexpected error occured.")
                return None
            
        #weather server was not reached 
        except requests.exceptions.RequestException:
            print("Unable to connect to the weather service.")
            return None
        

    def fahrenheit_to_celsius(self, temp_f):
        return (temp_f - 32) * 5/9
    
    def meters_to_miles(self, meters):
        return meters/ 1609.34

    def display_weather(self, data):
        if data is None:
            print("Unable to display weather")
            return
        
        city = data["name"]
        description = data["weather"][0]["description"]   
        temperature_f = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        visibility = data["visibility"]

        temperature_c = self.fahrenheit_to_celcsius(temperature_f)
        visibility_miles = self.meters_to_miles(visibility)


        print("Current Weather")
        print("------------------------")
        print(f"City: {city}")
        print(f"Condition: {description}")
        print(f"Temperature: {temperature_f:.2f} F")
        print(f"Temperature: {temperature_c:.2f} C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} mph")
        print(f"Visibilty: {visibility_miles:.1f} miles")

    def run(self):

        city = input("Enter a city: ").strip()

        if city == "":
            print("Please enter a city")
            return
        
        data = self.get_weather(city)

        if data is None:
            print("City not found")
            return
        
        self.display_weather(data)


class WeatherGUI:

    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Smart Weather System")
        self.root.geometry("650x500")

        self.aviation_weather = AviationWx()

        if api_key:
            self.general_weather = WeatherApp(api_key)
        else:
            self.general_weather = None

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Smart Weather System",
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
    