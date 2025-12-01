from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

NOMINATIM = "https://nominatim.openstreetmap.org"
UA = {"User-Agent": "VietnamDiscoveryExplorer/1.0 (educational-project; student@university.edu)"}
RADIUS_M = 5000
OVERPASS = "https://overpass-api.de/api/interpreter"
OPENWEATHER_API_KEY = ""
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

app = Flask(__name__)
CORS(app) 

class AttractionLocation:
    def __init__(self, name = "", lat = 0, lon = 0):
        self.name = name
        self.lat = lat
        self.lon = lon
        
    def getLocation(self):
        return (self.lat, self.lon)
    
    def setLocation(self, name, lat=None, lon=None):
        self.name = name
        if lat is not None:
            self.lat = lat
        if lon is not None:
            self.lon = lon
     
    @staticmethod
    def geocode(query: str):
        try:
            time.sleep(1.0)
            r = requests.get(f"{NOMINATIM}/search", params={"q": query, "format": "jsonv2", "limit": 1, "addressdetails": 1}, headers=UA, timeout=60)
            r.raise_for_status()
            data = r.json()
            if not data: 
                raise ValueError("Location not found in Vietnam")
            item = data[0]
            return float(item["lat"]), float(item["lon"])
        except Exception as e:
            raise ValueError(f"Geocoding error: {str(e)}")
    
    def find_five_interest_location(self):
        QL = f"""
        [out:json][timeout:25];
        (
          // Tourism attractions
          nwr(around:{RADIUS_M},{self.lat},{self.lon})["tourism"~"^(attraction)$"];
        );
        out center 25;
        """
        try:
            time.sleep(1.0)
            
            r = requests.post(OVERPASS, data=QL.encode("utf-8"), headers=UA, timeout=30)
            r.raise_for_status()
            data = r.json().get("elements", [])
        except Exception as e:
            print(f"Error querying Overpass API: {str(e)}")
            return []
        
        location_list = []
        seen_names = set()  # Avoid duplicates
        
        for element in data:
            try:
                # Get coordinates
                lat = element.get("lat") or (element.get("center", {}).get("lat"))
                lon = element.get("lon") or (element.get("center", {}).get("lon"))
                
                if not (lat and lon):
                    continue
                
                # Get tags
                tags = element.get("tags", {})
                if not tags:
                    continue
                
                # Get name
                name = tags.get("name", tags.get("name:en", "Unknown Location"))
                
                # Skip if we've seen this name before or it's generic
                if name in seen_names or name in ["Unknown Location", ""]:
                    continue
                
                seen_names.add(name)
                
                # Determine type
                location_type = (
                    tags.get("tourism") or 
                    tags.get("amenity") or 
                    tags.get("historic") or 
                    tags.get("leisure") or 
                    "attraction"
                )
                
                location_list.append({
                    "name": name,
                    "lat": float(lat),
                    "lon": float(lon),
                    "type": location_type,
                    "tags": tags
                })
                
                # Stop when we have enough results
                if len(location_list) >= 5:
                    break
                    
            except (KeyError, ValueError, TypeError):
                continue
        
        return location_list

def get_weather_data(lat, lon, location_name):
    """
    Fetch current weather and 5-day forecast for the given coordinates
    """
    try:
        # Get current weather
        current_url = f"{OPENWEATHER_BASE_URL}/weather"
        current_params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "en"
        }
        
        current_response = requests.get(current_url, params=current_params, timeout=10)
        current_response.raise_for_status()
        current_data = current_response.json()
        
        # Get 5-day forecast
        forecast_url = f"{OPENWEATHER_BASE_URL}/forecast"
        forecast_params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "en"
        }
        
        forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Process forecast data - get one forecast per day (noon time)
        daily_forecasts = []
        seen_dates = set()
        
        for item in forecast_data.get("list", []):
            date = item["dt_txt"].split(" ")[0]  # Get date part
            time_part = item["dt_txt"].split(" ")[1]  # Get time part
            
            # Take the forecast closest to noon (12:00:00) for each day
            if date not in seen_dates and "12:00:00" in time_part:
                daily_forecasts.append({
                    "date": date,
                    "temp": round(item["main"]["temp"]),
                    "temp_min": round(item["main"]["temp_min"]),
                    "temp_max": round(item["main"]["temp_max"]),
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": round(item["wind"]["speed"], 1)
                })
                seen_dates.add(date)
                
                # Limit to 5 days
                if len(daily_forecasts) >= 5:
                    break
        
        # Format current weather
        weather_info = {
            "current": {
                "location": location_name,
                "temperature": round(current_data["main"]["temp"]),
                "feels_like": round(current_data["main"]["feels_like"]),
                "description": current_data["weather"][0]["description"].title(),
                "icon": current_data["weather"][0]["icon"],
                "humidity": current_data["main"]["humidity"],
                "pressure": current_data["main"]["pressure"],
                "wind_speed": round(current_data["wind"]["speed"], 1),
                "wind_direction": current_data["wind"].get("deg", 0),
                "visibility": current_data.get("visibility", 0) / 1000,  # Convert to km
                "uv_index": current_data.get("uvi", "N/A"),
                "sunrise": current_data["sys"]["sunrise"],
                "sunset": current_data["sys"]["sunset"]
            },
            "forecast": daily_forecasts
        }
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API request error: {str(e)}")
        return None
    except Exception as e:
        print(f"Weather data processing error: {str(e)}")
        return None

@app.route('/api/search', methods=['POST'])
def search_destination():
    try:
        data = request.get_json()
        
        if not data or 'destination' not in data:
            return jsonify({
                'success': False,
                'message': 'Please provide a destination to explore'
            }), 400
        
        destination = data['destination'].strip()
        
        if not destination:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid Vietnamese destination'
            }), 400
        
        # Geocode the destination
        try:
            lat, lon = AttractionLocation.geocode(destination)
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 404
        
        # Create location object with geocoded coordinates
        location = AttractionLocation(destination, lat, lon)
        attractions = location.find_five_interest_location()
        
        # Get weather data for the destination
        weather_data = get_weather_data(lat, lon, destination)
        
        response_data = {
            'success': True,
            'location': {
                'lat': lat,
                'lon': lon
            },
            'attractions': attractions,
            'message': f'Discovered {len(attractions)} amazing attractions for your exploration!'
        }
        
        # Add weather data if available
        if weather_data:
            response_data['weather'] = weather_data
            response_data['message'] += f' Weather information included for {destination}.'
        else:
            response_data['weather'] = None
            response_data['message'] += ' (Weather data temporarily unavailable)'
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
        
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Vietnam Discovery Explorer API is running smoothly'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Vietnam Discovery Explorer API - Explore the beauty of Vietnam!',
        'version': '1.0.0',
        'endpoints': {
            'search': '/api/search (POST) - Discover attractions in Vietnamese destinations',
            'health': '/api/health (GET) - Check API status'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    