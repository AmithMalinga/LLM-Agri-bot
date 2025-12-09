# Creating Your Custom Chatbot: Unleashing the Power of Groq API and HuggingFace for Text and Voice Interactions

Gone are the days of one-size-fits-all chatbots that lack personalization and fail to engage users effectively. Today, we have the opportunity to create chatbots that truly understand and connect with their audience. With Groq API, we can tap into the state-of-the-art language model, allowing our chatbot to comprehend natural language inputs, provide accurate responses, and even hold dynamic conversations with users.

## ✨ New Feature: Real-Time Weather Integration

The AgriBot now includes **real-time weather data** to provide context-aware farming advice! Simply enter your location and get:
- 🌡️ Current temperature and feels-like temperature
- 💧 Humidity levels
- 💨 Wind speed
- 🌧️ Precipitation data
- 📊 Atmospheric pressure
- ☀️ Weather conditions with visual icons

The AI assistant automatically considers current weather conditions when providing farming recommendations!

![webview](https://github.com/mohammed97ashraf/LLM_Agri_Bot/blob/main/Sample_image/voicechat_web.png)

## 🚀 Features

- 🤖 **AI-Powered Chat**: Get intelligent farming advice using Groq's Llama 3.3 70B model
- 🌍 **Multi-Language Support**: English and Sinhala
- 🎤 **Voice Input**: Speech-to-text using HuggingFace
- 🔊 **Voice Output**: Text-to-speech responses
- ☁️ **Weather Integration**: Real-time weather data for location-based farming advice
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 📋 How To Run Locally:

1. **Clone this repository**
   ```bash
   git clone https://github.com/mohammed97ashraf/LLM_Agri_Bot.git
   cd LLM_Agri_Bot
   ```

2. **Install All The Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```
     hugging_face=your_huggingface_api_key_here
     groq_api_key=your_groq_api_key_here
     ```
   - Get your keys from:
     - [Groq API](https://console.groq.com/) - Free tier available
     - [HuggingFace](https://huggingface.co/settings/tokens) - Free

4. **Run The Application**
   ```bash
   python app.py
   ```

5. **Open Your Browser**
   - Navigate to `http://localhost:5000`
   - Select your language
   - Enter your location for weather-aware farming advice
   - Start chatting!

## 🌤️ Using the Weather Feature

1. Enter your location in the weather widget (e.g., "Mumbai", "Bangalore", "Delhi", "New York")
2. Click "Get Weather" to fetch current conditions
3. The AI will automatically consider weather data when answering your farming questions
4. Weather data is sourced from **Open-Meteo API** (free, reliable, no API key needed)

## 💡 Example Questions

- "What crops should I plant this season?" (considers current weather)
- "Is it a good time for irrigation?"
- "How should I protect my crops from this weather?"
- "What fertilizer should I use for wheat?"

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **AI Model**: Groq Llama 3.3 70B
- **Speech-to-Text**: HuggingFace Wav2Vec2
- **Text-to-Speech**: Google TTS (gTTS)
- **Weather API**: Open-Meteo (free, no API key required)
- **Frontend**: HTML, CSS, JavaScript, jQuery

## 📚 API Documentation

### Weather Endpoint
```
POST /weather
Content-Type: application/json

{
  "location": "Mumbai"
}
```

### Chat Endpoint
```
POST /chat
Content-Type: application/x-www-form-urlencoded

text=your_question&language=en&location=Mumbai
```

## 🔒 Security Notes

- Never commit your `.env` file
- Keep your API keys secure
- Use environment variables for all sensitive data

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## [Read More at medium](https://medium.com/@mohammed97ashraf/creating-your-custom-chatbot-unleashing-the-power-of-openai-api-and-huggingface-for-text-and-voice-ccfbd39d6178)

