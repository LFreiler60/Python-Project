import requests 




class AviationWx:

    #init to store url incase add other functions such as taf or pireps
    def __init__(self):
        self.metar_url = "https://aviationweather.gov/api/data/metar"


    #hours included for ml data collection
    def get_metar(self, station_id, hours=1):
        parameters = {
             "ids" : station_id,
             "format" : "json",
             "hours" : hours,
        }

        try:    #requests.get(url, params)
            metar_data = requests.get(
                self.metar_url,
                params = parameters,
                headers={"User-Agent": "AviationWeatherPredictor/0.1"},
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
