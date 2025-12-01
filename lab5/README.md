# 🌟 Vietnam Discovery Explorer

A comprehensive web application for exploring Vietnam's beautiful destinations and discovering amazing points of interest in Vietnamese cities and locations.

![Vietnam Discovery](https://img.shields.io/badge/Vietnam-Discovery-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-3.0+-red)
![React](https://img.shields.io/badge/React-18+-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)

## ✨ Features

- **🔍 Smart Search**: Search any Vietnamese city or destination with intelligent geocoding
- **🗺️ Interactive Map**: Beautiful Leaflet maps with custom markers and smooth navigation
- **🎯 Attraction Discovery**: Automatically discover up to 5 fascinating points of interest nearby
- **📍 Visual Markers**: Special icons distinguishing main destinations from attractions
- **🌐 Real-time Data**: Powered by OpenStreetMap and Nominatim APIs for accurate information
- **📱 Responsive Design**: Works seamlessly on both desktop and mobile devices
- **🎨 Modern Interface**: Clean, intuitive UI with smooth animations and visual feedback

## 🚀 Quick Start

### System Requirements

- Python 3.8+ installed
- Node.js 16+ (for React development)
- Modern web browser with JavaScript support

### Installation & Setup

1. **Install Python Dependencies**

   ```bash
   pip install flask flask-cors requests
   ```

2. **Start the Flask Backend**

   ```bash
   cd src
   python main.py
   ```
   The API server will run at `http://localhost:5000`

3. **Launch the Application**
   - **Method 1 (Simple)**: Open `src/index.html` directly in your web browser
   - **Method 2 (React Development)**: For development with hot reload:

     ```bash
     npm install
     npm start
     ```

## 🎮 How to Use

### Basic Usage

1. **Open the application** in your web browser
2. **Enter a Vietnamese destination** (e.g., "Da Nang", "Hue", "Nha Trang", "Can Tho")
3. **Click Explore** or press Enter
4. **Navigate the interactive map** showing your destination and nearby attractions
5. **Click on markers** to view detailed information about each location

### Search Examples

- `Da Nang` - Central coastal city with beautiful beaches
- `Hue` - Former imperial capital with rich history
- `Nha Trang` - Popular beach destination
- `Hoi An` - UNESCO World Heritage ancient town
- `Can Tho` - Heart of the Mekong Delta region

## 🏗️ Architecture

### Frontend (React + TypeScript)

```
src/
├── App.tsx          # Main application component with state management
├── Map.tsx          # Interactive Leaflet map component  
├── SearchPanel.tsx  # Search interface and user controls
├── index.html       # Standalone HTML version
└── index.css        # Modern styling and smooth animations
```

### Backend (Flask + Python)

```
src/
└── main.py          # Flask API server
    ├── AttractionLocation class  # Location handling and geocoding
    ├── Geocoding service         # Nominatim integration
    ├── Attraction finder         # Overpass API integration
    └── REST API endpoints        # Search and health endpoints
```

## 🔧 API Endpoints

### `POST /api/search`
Search for a destination and discover nearby attractions.

**Request:**
```json
{
  "destination": "Da Nang"
}
```

**Response:**
```json
{
  "success": true,
  "location": {
    "lat": 21.0285,
    "lon": 105.8542
  },
  "attractions": [
    {
      "name": "Dragon Bridge",
      "lat": 16.0678,
      "lon": 108.2340,
      "type": "attraction"
    }
  ],
  "message": "Discovered 5 amazing attractions for your exploration!"
}
```

### `GET /api/health`

Check the API server status and health.

**Response:**

```json
{
  "status": "healthy",
  "message": "Vietnam Discovery Explorer API is running smoothly"
}
```

## 🎨 Customization

### Custom Marker Icons
Customize marker appearance in your components:

```javascript
const destinationIcon = L.divIcon({
    html: '<div class="marker-icon destination-icon">📍</div>',
    className: 'custom-marker',
    iconSize: [40, 40],
    iconAnchor: [20, 40]
});

const attractionIcon = L.divIcon({
    html: '<div class="marker-icon attraction-icon">🎯</div>',
    className: 'custom-marker',
    iconSize: [35, 35],
    iconAnchor: [17, 35]
});
```

### Custom Styling

Modify `index.css` to customize colors, animations, and layout:

```css
.destination-icon {
    background: linear-gradient(135deg, #ff4444, #ff6666);
    /* Your custom styles here */
}

.attraction-icon {
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    animation: pulse 3s infinite;
    /* Your custom styles here */
}
```

### Search Radius Configuration

Adjust the search radius in `main.py`:

```python
RADIUS_M = 5000  # 5km radius (modify as needed)
```

## 📦 Dependencies

### Python Backend

- `flask` - Web framework
- `flask-cors` - Cross-Origin Resource Sharing
- `requests` - HTTP library cho API calls

### Frontend

- `leaflet` - Interactive mapping library
- `react` - UI framework (for React version)
- `typescript` - Type safety and better development experience

## 🌐 External APIs

- **OpenStreetMap**: Map tiles and geographical data
- **Nominatim**: Geocoding service (converts location names to coordinates)
- **Overpass API**: Query OpenStreetMap data to find points of interest

## 🎯 Vietnam-Focused Features

### Vietnamese Location Support

The application specializes in Vietnamese destinations:

- **Major Cities**: Ho Chi Minh City, Hanoi, Da Nang, Hai Phong
- **Tourist Destinations**: Ha Long Bay, Sapa, Hoi An, Phu Quoc, Nha Trang
- **Provincial Areas**: Can Tho, Hue, Quy Nhon, Vung Tau

### Supported Attraction Types

- 🏛️ **Historical Sites**: Temples, pagodas, imperial tombs, monuments
- 🌊 **Natural Attractions**: Lakes, rivers, mountains, beaches, national parks
- 🍜 **Culinary Spots**: Restaurants, coffee shops, street food markets
- 🛍️ **Shopping Areas**: Traditional markets, shopping centers, local boutiques
- 🎨 **Cultural Sites**: Museums, art galleries, theaters, cultural centers

**NOTE:**   

**GitHub Copilot**. **Copilot, GitHub via Visual Studio Code**, truy cập 3h55 16/11/2025,
prompt: “tạo cho tôi 1 UI/ UX hoàn thiện bằng cách đọc và cải tiến file index.html, index.css”, dùng để sinh UI/UX, AI tạo phần search_bar và main screen 

**GitHub Copilot**. **Copilot, GitHub via Visual Studio Code**, truy cập 19h 16/11/2025,
prompt: “kiểm tra tôi file main.py cần cải tiến gì”, dùng để tối ưu tìm location, AI thêm điều kiện và tối ưu code để tìm location nhanh hơn
