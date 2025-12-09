import os
from flask import Flask, render_template, request, jsonify,url_for
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from groq import Groq
import requests
from gtts import gTTS
import asyncio
import string
import random
from datetime import datetime


#load the api keys from the the .env file
load_dotenv()
#
hugging_face = os.getenv('hugging_face')
groq_api_key = os.getenv('groq_api_key')
#
client = Groq(api_key=groq_api_key)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'webm'}

# Weather API function using Open-Meteo (completely free, no API key)
def get_weather_data(location):
    try:
        # Step 1: Get coordinates from location name using Open-Meteo Geocoding
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        
        if geo_response.status_code != 200:
            print(f"Geocoding failed: {geo_response.status_code}")
            return None
            
        geo_data = geo_response.json()
        
        if 'results' not in geo_data or len(geo_data['results']) == 0:
            print(f"Location not found: {location}")
            return None
        
        # Get first result
        place = geo_data['results'][0]
        latitude = place['latitude']
        longitude = place['longitude']
        location_name = place['name']
        country = place.get('country', '')
        
        # Step 2: Get weather data using coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,surface_pressure&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        
        if weather_response.status_code != 200:
            print(f"Weather API failed: {weather_response.status_code}")
            return None
            
        weather_data = weather_response.json()
        current = weather_data['current']
        
        # Map weather code to description and icon
        weather_code = current['weather_code']
        description, icon = get_weather_info(weather_code)
        
        weather_info = {
            'location': f"{location_name}, {country}",
            'temperature': str(round(current['temperature_2m'])),
            'feels_like': str(round(current['apparent_temperature'])),
            'humidity': str(current['relative_humidity_2m']),
            'description': description,
            'wind_speed': str(round(current['wind_speed_10m'])),
            'pressure': str(round(current['surface_pressure'])),
            'precipitation': str(current['precipitation']),
            'icon': icon,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        return weather_info
        
    except requests.exceptions.Timeout:
        print("Weather API timeout")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Weather API request error: {e}")
        return None
    except Exception as e:
        print(f"Weather API Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_weather_info(weather_code):
    """Map WMO weather codes to descriptions and icons"""
    weather_map = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Depositing rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Moderate drizzle", "🌦️"),
        55: ("Dense drizzle", "🌧️"),
        56: ("Light freezing drizzle", "🌧️"),
        57: ("Dense freezing drizzle", "🌧️"),
        61: ("Slight rain", "🌧️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        66: ("Light freezing rain", "🌧️"),
        67: ("Heavy freezing rain", "🌧️"),
        71: ("Slight snow", "🌨️"),
        73: ("Moderate snow", "❄️"),
        75: ("Heavy snow", "❄️"),
        77: ("Snow grains", "❄️"),
        80: ("Slight rain showers", "🌦️"),
        81: ("Moderate rain showers", "🌧️"),
        82: ("Violent rain showers", "⛈️"),
        85: ("Slight snow showers", "🌨️"),
        86: ("Heavy snow showers", "❄️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with slight hail", "⛈️"),
        99: ("Thunderstorm with heavy hail", "⛈️"),
    }
    
    return weather_map.get(weather_code, ("Unknown", "🌡️"))


def get_anwer_openai(question, system_prompt=None, language='en', weather_context=None):
    if system_prompt is None:
        system_prompt = "You are a helpful agriculture chatbot assisting farmers with their queries. Respond in English."
    
    # Add weather context to system prompt if available
    if weather_context:
        weather_info = f"\n\nCurrent Weather Information for {weather_context['location']}:\n"
        weather_info += f"Temperature: {weather_context['temperature']}°C (Feels like {weather_context['feels_like']}°C)\n"
        weather_info += f"Condition: {weather_context['description']}\n"
        weather_info += f"Humidity: {weather_context['humidity']}%\n"
        weather_info += f"Wind Speed: {weather_context['wind_speed']} km/h\n"
        weather_info += f"Precipitation: {weather_context['precipitation']} mm\n"
        weather_info += "\nPlease consider this current weather data when providing farming advice."
        system_prompt += weather_info
    
    completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages = [{"role": "system", "content" : system_prompt},
                            {"role": "user", "content" : "Give a Brief Of Agriculture Seasons in India"},
                            {"role":"assistant","content":"In India, the agricultural season consists of three major seasons: the Kharif (monsoon), the Rabi (winter), and the Zaid (summer) seasons. Each season has its own specific crops and farming practices.\n\n1. Kharif Season (Monsoon Season):\nThe Kharif season typically starts in June and lasts until September. This season is characterized by the onset of the monsoon rains, which are crucial for agricultural activities in several parts of the country. Major crops grown during this season include rice, maize, jowar (sorghum), bajra (pearl millet), cotton, groundnut, turmeric, and sugarcane. These crops thrive in the rainy conditions and are often referred to as rain-fed crops.\n\n2. Rabi Season (Winter Season):\nThe Rabi season usually spans from October to March. This season is characterized by cooler temperatures and lesser or no rainfall. Crops grown during the Rabi season are generally sown in October and harvested in March-April. The major Rabi crops include wheat, barley, mustard, peas, gram (chickpeas), linseed, and coriander. These crops rely mostly on irrigation and are well-suited for the drier winter conditions.\n\n3. Zaid Season (Summer Season):\nThe Zaid season occurs between March and June and is a transitional period between Rabi and Kharif seasons. This season is marked by warmer temperatures and relatively less rainfall. The Zaid crops are grown during this time and include vegetables like cucumber, watermelon, muskmelon, bottle gourd, bitter gourd, and leafy greens such as spinach and amaranth. These crops are generally irrigated and have a shorter growing period compared to Kharif and Rabi crops.\n\nThese three agricultural seasons play a significant role in India's agricultural economy and provide stability to food production throughout the year. Farmers adapt their farming practices and crop selection accordingly to make the best use of the prevailing climatic conditions in each season."},
                            {"role":"user","content":question}
                ]
            )
    
    return completion.choices[0].message.content


###





def text_to_audio(text, filename, language='en'):
    # Map language codes to gTTS language codes
    lang_map = {
        'en': 'en',
        'si': 'si'  # Sinhala
    }
    tts_lang = lang_map.get(language, 'en')
    tts = gTTS(text, lang=tts_lang)
    tts.save(f'static/audio/{filename}.mp3')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    location = data.get('location', '')
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    weather_data = get_weather_data(location)
    
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    if 'audio' in request.files:
        audio = request.files['audio']
        if audio and allowed_file(audio.filename):
            filename = secure_filename(audio.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)
            transcription = process_audio(filepath)
            return jsonify({'text': transcription})

    text = request.form.get('text')
    if text:
        language = request.form.get('language', 'en')
        system_prompt = request.form.get('system_prompt')
        location = request.form.get('location', '')
        
        # Get weather context if location provided
        weather_context = None
        if location:
            weather_context = get_weather_data(location)
        
        response = process_text(text, language, system_prompt, weather_context)
        return {'text': response['text'],'voice': url_for('static', filename='audio/' + response['voice'])}

    return jsonify({'text': 'Invalid request'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_audio(filepath):
    # Placeholder function for processing audio (speech-to-text transcription)
    # Replace this with your own implementation using libraries like SpeechRecognition or DeepSpeech
    #return 'hello This is a placeholder transcription for audio'
    API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
    headers = {"Authorization": hugging_face}
    with open(filepath, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    data = response.json()
    return data['text']
    

def process_text(text, language='en', system_prompt=None, weather_context=None):
    # Get AI response with language context and weather data
    return_text = get_anwer_openai(text, system_prompt, language, weather_context)
    
    # Generate random filename
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Generate audio in the appropriate language
    text_to_audio(return_text, res, language)
    
    return {"text": return_text, "voice": f"{res}.mp3"}


if __name__ == '__main__':
    app.run(debug=True)

