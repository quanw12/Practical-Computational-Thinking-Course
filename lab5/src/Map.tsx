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

interface MapProps {
  center: Location;
  destination: string | null;
  attractions: Attraction[];
}

const Map: React.FC<MapProps> = ({ center, destination, attractions }) => {
  return (
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
      
      {/* Main destination marker (red) */}
      {destination && (
        <Marker position={[center.lat, center.lon]}>
          <Popup>
            <div>
              <strong>🎯 {destination}</strong>
              <br />
              Your Selected Destination
            </div>
          </Popup>
        </Marker>
      )}
      
      {/* Attraction markers (blue) */}
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
  );
};

export default Map;