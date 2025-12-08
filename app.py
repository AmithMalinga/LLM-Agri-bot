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


def get_anwer_openai(question, system_prompt=None, language='en'):
    if system_prompt is None:
        system_prompt = "You are a helpful agriculture chatbot assisting farmers with their queries. Respond in English."
    
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
        response = process_text(text, language, system_prompt)
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
    

def process_text(text, language='en', system_prompt=None):
    # Get AI response with language context
    return_text = get_anwer_openai(text, system_prompt, language)
    
    # Generate random filename
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Generate audio in the appropriate language
    text_to_audio(return_text, res, language)
    
    return {"text": return_text, "voice": f"{res}.mp3"}


if __name__ == '__main__':
    app.run(debug=True)

