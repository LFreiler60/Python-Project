import requests

class OpenWeatherService:
    #check for API here since aviationwx doesnt requier API key
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("OpenWeatherService requires an OpenWeather API key")

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
                params=parameters,
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
        
    @staticmethod 
    def fahrenheit_to_celsius(temp_f):
        return (temp_f - 32) * 5/9
    
    @staticmethod 
    def meters_to_miles(meters):
        return meters/ 1609.34

    def display_weather(self, data):
        if data is None:
            print("Unable to display weather")
            return

        #uses keys in dictionary to retrieve value
        city = data["name"]
        description = data["weather"][0]["description"]   
        temperature_f = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        visibility = data["visibility"]

        temperature_c = self.fahrenheit_to_celsius(temperature_f)
        visibility_miles = self.meters_to_miles(visibility)


        print("Current Weather")
        print("------------------------")
        print(f"City: {city}")
        print(f"Condition: {description}")
        print(f"Temperature: {temperature_f:.2f} F")
        print(f"Temperature: {temperature_c:.2f} C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} mph")
        print(f"Visibility: {visibility_miles:.1f} miles")

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