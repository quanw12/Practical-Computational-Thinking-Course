import React, { useState } from 'react';
import Map from './Map';
import SearchPanel from './SearchPanel';
import TranslationPanel from './TranslationPanel';
import './index.css';

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

function App() {
  const [center, setCenter] = useState<Location | null>(null); // No default location
  const [destination, setDestination] = useState<string | null>(null);
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false); // Track if user has searched

  const searchDestination = async (query: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ destination: query })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        // Update map center and destination
        setCenter({ lat: data.location.lat, lon: data.location.lon });
        setDestination(query);
        setAttractions(data.attractions || []);
        setWeather(data.weather || null);
        setHasSearched(true);
      } else {
        throw new Error(data.message || 'Location not found');
      }

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(`Error: ${errorMessage}`);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <SearchPanel 
        onSearch={searchDestination}
        loading={loading}
        error={error}
      />
      {hasSearched && center ? (
        <>
          <Map 
            center={center}
            destination={destination}
            attractions={attractions}
            weather={weather}
          />
          <TranslationPanel />
        </>
      ) : (
        <>
          <div className="welcome-message">
            <div className="welcome-content">
              <h1>🌟 Vietnam Discovery Explorer</h1>
              <p>Discover amazing destinations and explore Vietnam's hidden gems!</p>
              <div className="instructions">
                <p>🏞️ Enter any Vietnamese city or location above</p>
                <p>✨ Discover 5 amazing attractions and points of interest nearby</p>
                <p>🗺️ Navigate through Vietnam's beautiful landscapes</p>
                <p>🔤 Use the translation tool below to convert English to Vietnamese</p>
              </div>
            </div>
          </div>
          <TranslationPanel />
        </>
      )}
    </div>
  );
}

export default App;