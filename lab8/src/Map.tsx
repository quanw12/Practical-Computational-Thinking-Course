import React from 'react';
import { MapContainer, Popup, TileLayer, Marker } from "react-leaflet";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix default markers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface Location {
  lat: number;
  lon: number;
}

interface Attraction {
  name: string;
  lat: number;
  lon: number;
  type: string;
}

interface WeatherData {
  current: {
    location: string;
    temperature: number;
    feels_like: number;
    description: string;
    icon: string;
    humidity: number;
    pressure: number;
    wind_speed: number;
    wind_direction: number;
    visibility: number;
    uv_index: string | number;
    sunrise: number;
    sunset: number;
  };
  forecast: Array<{
    date: string;
    temp: number;
    temp_min: number;
    temp_max: number;
    description: string;
    icon: string;
    humidity: number;
    wind_speed: number;
  }>;
}

interface MapProps {
  center: Location;
  destination: string | null;
  attractions: Attraction[];
  weather: WeatherData | null;
}

const Map: React.FC<MapProps> = ({ center, destination, attractions, weather }) => {
  const formatTime = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
  };

  return (
    <div style={{ position: 'relative', height: '100vh', width: '100%' }}>
      <MapContainer 
        center={[center.lat, center.lon]} 
        zoom={13} 
        scrollWheelZoom={true}
        style={{ height: "100vh", width: "100%" }}
        key={`${center.lat}-${center.lon}`} 
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Main destination marker with weather info */}
        {destination && (
          <Marker position={[center.lat, center.lon]}>
            <Popup maxWidth={300}>
              <div style={{ minWidth: '250px' }}>
                <strong>🎯 {destination}</strong>
                <br />
                <small>Your Selected Destination</small>
                
                {weather && weather.current && (
                  <div className="weather-popup">
                    <div className="weather-popup-header">
                      <img 
                        src={`https://openweathermap.org/img/wn/${weather.current.icon}@2x.png`} 
                        alt={weather.current.description}
                        style={{ width: '50px', height: '50px' }}
                      />
                      <div>
                        <div className="weather-popup-temp">
                          {weather.current.temperature}°C
                        </div>
                        <div className="weather-popup-feels">
                          Feels like {weather.current.feels_like}°C
                        </div>
                      </div>
                    </div>
                    
                    <div className="weather-popup-desc">
                      {weather.current.description}
                    </div>
                    
                    <div className="weather-popup-details">
                      <div>💧 Humidity: {weather.current.humidity}%</div>
                      <div>💨 Wind: {weather.current.wind_speed} m/s</div>
                      <div>👁️ Visibility: {weather.current.visibility} km</div>
                      <div>🌅 Sunrise: {formatTime(weather.current.sunrise)}</div>
                      <div>🌇 Sunset: {formatTime(weather.current.sunset)}</div>
                    </div>
                  </div>
                )}
              </div>
            </Popup>
          </Marker>
        )}
        
        {/* Attraction markers */}
        {attractions.map((attraction, index) => (
          <Marker 
            key={index} 
            position={[attraction.lat, attraction.lon]} 
          >
            <Popup>
              <div>
                <strong>✨ {attraction.name}</strong>
                <br />
                Category: {attraction.type}
                <br />
                <small>Point of Interest</small>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Weather panel */}
      {weather && (
        <div className="weather-panel">
          <h3>
            🌤️ Weather in {destination}
          </h3>
          
          {/* Current Weather */}
          <div className="current-weather">
            <img 
              src={`https://openweathermap.org/img/wn/${weather.current.icon}@2x.png`} 
              alt={weather.current.description}
            />
            <div>
              <div className="current-temp">
                {weather.current.temperature}°C
              </div>
              <div className="current-desc">
                {weather.current.description}
              </div>
            </div>
          </div>
          
          {/* 5-day forecast */}
          {weather.forecast && weather.forecast.length > 0 && (
            <div className="forecast-section">
              <h4>5-Day Forecast</h4>
              <div>
                {weather.forecast.map((day, index) => (
                  <div key={index} className="forecast-day">
                    <span className="forecast-date">{formatDate(day.date)}</span>
                    <img 
                      src={`https://openweathermap.org/img/wn/${day.icon}.png`} 
                      alt={day.description}
                      className="forecast-icon"
                    />
                    <span className="forecast-temp">
                      {day.temp_max}°/{day.temp_min}°
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Map;