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


<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Airly</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    html, body {
      height: 100%;
    }

    body {
      font-family: 'Playfair Display', serif;

      background-image: url("bg.png");
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;

      color: white;
    }

    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 20px 40px;
      position: relative;
    }

    .menu {
      font-size: 28px;
      cursor: pointer;
    }

    .nav-links {
      display: flex;
      gap: 40px;
      font-size: 22px;
      font-style: italic;
    }

    .dropdown {
      position: absolute;
      top: 70px;
      left: 40px;
      background: white;
      color: black;
      border-radius: 10px;
      display: none;
      overflow: hidden;
      box-shadow: 0 8px 20px rgba(0,0,0,0.25);
      z-index: 10;
    }

    .dropdown div {
      padding: 14px 22px;
      cursor: pointer;
      font-size: 18px;
    }

    .dropdown div:hover {
      background: #f2f2f2;
    }

    .title {
      text-align: center;
      margin-top: 40px;
      font-size: 70px;
      font-weight: 700;
    }

    .city-container {
      margin-top: 60px;
      padding: 0 60px;
      display: flex;
      justify-content: space-between;
    }

    .cities {
      display: flex;
      flex-direction: column;
      gap: 22px;
      font-size: 22px;
    }

    .city span {
      font-size: 26px;
    }

    .arrows {
      display: flex;
      flex-direction: column;
      gap: 32px;
      font-size: 26px;
      cursor: pointer;
    }

    .feedback {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: white;
      color: black;
      padding: 12px 18px;
      border-radius: 30px;
      font-size: 14px;
      cursor: pointer;
    }

    @media (max-width: 768px) {
      .title {
        font-size: 48px;
      }

      .nav-links {
        font-size: 18px;
        gap: 20px;
      }

      .city-container {
        padding: 0 30px;
      }
    }
  </style>
</head>

<body>

  <div class="navbar">
    <div class="menu" id="menuBtn">☰</div>

    <div class="nav-links">
      <div>Home</div>
      <div>Activity</div>
      <div>Tips</div>>
    </div>

    <div class="dropdown" id="dropdown">
      <div>Delhi</div>
      <div>Bangalore</div>
      <div>Mumbai</div>
      <div>Hyderabad</div>
      <div>Kolkata</div>
    </div>
  </div>

  <div class="title">Airly</div>

  <div class="city-container">
    <div class="cities">
      <div class="city"><span>X°</span> Delhi</div>
      <div class="city"><span>X°</span> Bangalore</div>
      <div class="city"><span>X°</span> Mumbai</div>
      <div class="city"><span>X°</span> Hyderabad</div>
      <div class="city"><span>X°</span> Kolkata</div>
    </div>

    <div class="arrows">
      <div>➤</div>
      <div>➤</div>
      <div>➤</div>
      <div>➤</div>
      <div>➤</div>
    </div>
  </div>

  <div class="feedback">Feedback</div>

  <script>
    const menuBtn = document.getElementById("menuBtn");
    const dropdown = document.getElementById("dropdown");

    menuBtn.addEventListener("click", () => {
      dropdown.style.display =
        dropdown.style.display === "block" ? "none" : "block";
    });
  </script>

</body>
</html>





    
    
