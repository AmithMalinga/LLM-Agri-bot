# Weather Integration Feature Guide

## 🌤️ Overview
The AgriBot now includes real-time weather integration to provide context-aware farming advice based on current weather conditions.

## 🔧 Technical Implementation

### Backend (app.py)
- **Weather API**: Uses wttr.in (free, no API key required)
- **Endpoint**: `/weather` (POST)
- **Function**: `get_weather_data(location)`
- **Weather Context**: Automatically passed to AI when location is set

### Frontend (index.html)
- **Weather Widget**: Displays at the top of the chat interface
- **Real-time Updates**: Fetches weather on button click
- **Auto-Integration**: Weather data automatically included in chat context

## 📊 Weather Data Provided

1. **Temperature**: Current and "feels like" temperature in Celsius
2. **Humidity**: Current humidity percentage
3. **Wind Speed**: Wind speed in km/h
4. **Precipitation**: Rainfall in mm
5. **Pressure**: Atmospheric pressure in mb
6. **Description**: Weather condition description
7. **Icon**: Visual weather icon (emoji-based)

## 🎯 How It Works

1. User enters location (city name, region, or coordinates)
2. System fetches weather data from wttr.in API
3. Weather information is displayed in the widget
4. When user asks a farming question, weather context is automatically included
5. AI considers weather data when providing farming advice

## 💻 Code Structure

### Weather API Function
```python
def get_weather_data(location):
    # Fetches weather from wttr.in
    # Returns: temperature, humidity, wind, precipitation, etc.
```

### Weather Icon Mapping
```python
def get_weather_icon(weather_code):
    # Maps weather codes to emoji icons
    # Returns: emoji representing weather condition
```

### AI Integration
```python
def get_anwer_openai(question, system_prompt, language, weather_context):
    # Includes weather data in system prompt
    # AI uses weather context for farming advice
```

## 🌐 Supported Location Formats

- City name: "Mumbai", "Delhi", "Bangalore"
- Region: "Maharashtra", "Karnataka"
- City, Country: "Mumbai, India"
- Coordinates: "19.0760,72.8777"

## 🎨 UI Components

### Weather Widget Features
- **Input Field**: Enter location
- **Get Weather Button**: Fetch current weather
- **Weather Display**: Shows all weather metrics
- **Visual Icons**: Emoji-based weather icons
- **Timestamp**: Last updated time

### Styling
- Responsive design
- Mobile-friendly
- Smooth animations
- Clear visual hierarchy
- Integrated with chat interface

## 🔄 API Flow

```
User Input (Location) 
    ↓
Frontend (AJAX POST to /weather)
    ↓
Backend (get_weather_data)
    ↓
wttr.in API
    ↓
Weather Data Processing
    ↓
Return to Frontend
    ↓
Display in Weather Widget
    ↓
Include in Chat Context (when user asks questions)
```

## ⚠️ Error Handling

- Invalid location: Shows error message
- Network timeout: Graceful fallback
- API unavailable: User-friendly error
- No location set: Chat works normally without weather context

## 🚀 Future Enhancements

Potential improvements:
- Multi-day forecast
- Weather alerts for farmers
- Historical weather data
- Soil moisture predictions
- Crop-specific weather recommendations
- Weather-based irrigation scheduling
- Pest/disease risk based on weather
- Location auto-detection (geolocation)

## 📝 Usage Examples

### Simple Weather Query
```
Location: Mumbai
Result: Shows current weather with all metrics
```

### Weather-Aware Chat
```
User: "Should I irrigate my crops today?"
AI: Considers current weather (e.g., recent rainfall, humidity)
     Provides context-aware irrigation advice
```

### Multi-Location Usage
```
User can change location anytime
Weather context updates automatically
AI adapts advice to new location's weather
```

## 🔒 Privacy & Security

- No user data stored
- No API key required for weather
- Location data not logged
- All requests are stateless

## 📊 Performance

- Weather API response: ~1-2 seconds
- No rate limiting (wttr.in is very generous)
- Lightweight JSON response
- Efficient caching possible (future enhancement)

## 🐛 Troubleshooting

**Weather not loading?**
- Check internet connection
- Verify location spelling
- Try different location format
- Check browser console for errors

**Weather data incorrect?**
- Data comes from wttr.in
- Usually very accurate
- Updates every hour
- May vary by location coverage

**Location not found?**
- Try city name only
- Add country name
- Use larger nearby city
- Check spelling

## 📚 Resources

- wttr.in API: https://wttr.in/:help
- Weather codes: See `get_weather_icon()` function
- Flask documentation: https://flask.palletsprojects.com/
