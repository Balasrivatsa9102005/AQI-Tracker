from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "af07a54be8c7f8f9b0a4b2060e21da2a"  

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form.get('city')
        
        if not city or city.strip() == "":
            return render_template('index.html', error="Please enter a city name.")
        
        
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        
        if geo_response.status_code != 200 or not geo_response.json():
            return render_template('index.html', error="City not found or API error.")
        
        location_data = geo_response.json()[0]
        lat = location_data['lat']
        lon = location_data['lon']
        city_name = location_data.get('name', city)
        country = location_data.get('country', '')
        
        
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        pollution_response = requests.get(pollution_url)
        data = pollution_response.json()

        if pollution_response.status_code != 200 or "list" not in data:
            return render_template('index.html', error="Failed to fetch pollution data.")
        
        components = data['list'][0]['components']
        aqi = data['list'][0]['main']['aqi']
        
        
        date = datetime.fromtimestamp(data['list'][0]['dt']).strftime('%Y-%m-%d %H:%M:%S')
        
        aqi_labels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        aqi_label = aqi_labels.get(aqi, "Unknown")
        
        return render_template('index.html', 
                            city=city_name.title(),
                            country=country,
                            lat=lat,
                            lon=lon,
                            date=date, 
                            aqi=aqi, 
                            aqi_label=aqi_label, 
                            components=components)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)