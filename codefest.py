#Libraries
from flask import Flask, render_template, request
import requests
app = Flask(__name__)
API_KEY = "98284da501aa12de56f8e74f07155135"

#This is a function that defines the parameters of the aqi and what we can do in that aqi
def aqi_parameters(aqi):
    if aqi<=50:
        return "Air this clean doesn’t come every day — open those windows!"
    elif aqi<=100:
        return "Light exercise outdoors is fine, just avoid peak traffic roads."
    elif aqi<=200:
        return "Air quality is manageable, but indoor workouts masy feel better."
    else:
        return "Masks help, especially near traffic-heavy areas."
#This is basically for the webpage where the app would get the city from the dropdown thing the user selcts and then post it for python
@app.route("/", methods=["GET","POST"])

#This defines a funtion for the homepage and sets it as blank right now to add the data to
def home():
        data = none
    #basically it will upload the choice of city from the user
        if request.method == "POST":
            city = request.form["city"]

            # loctions into longitude and latititude
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo_data = requests.get(geo_url).json()
#this is to understand the lontidutdes and latititudes mentioned and gotten,
            if geo_data:
                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]

               #This will get the AQI data from the api. 
                aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
                aqi_data=requests.get(aqi_url).json()
                #grabs the aqi number from the api
                aqi = aqi_data["list"][0]["main"]["aqi"]

#this basically does the same but it grabs the weather from the api.
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                weather = requests.get(weather_url).json()
#this is the final classification of the AQI
                category, advice = classify_aqi()

#This is basically a dictionary that is putting together all thedata and it will help the HTML designing of the opage.
                data = {
                    "city": city,
                    "aqi": aqi,
                    "category": category,
                    "advice": advice,
                    "temp": weather["main"]["temp"],
                    "humidity": weather["main"]["humidity"]
                    "wind": weather["wind"]["speed"]
                 }

    #This is basically to help start the HTML code for the front end
    return render_template("index.html", data=data)

#this is checking if the main page's name is main and then it will hold true for the rest of the code.
if __name__ == "__main__":
    app.run(debug=True)


