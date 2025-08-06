import os
import pyttsx3
import speech_recognition as sr
import datetime
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎤 Voice Output: Speak text aloud
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS Error] {e}")

# 🎙️ Voice Input: Capture user's voice
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        query = r.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, the speech service is down.")
        return ""

# 🧠 Ask Gemini: Send user input + history to Gemini
def ask_gemini(prompt, chat_history):
    formatted_history = "\n".join(chat_history)
    full_prompt = f"{formatted_history}\nUser: {prompt}\nGemini:"
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "Sorry, I couldn't get a response from Gemini."

# 📝 Logging: Save interaction to a JSON file
def log_interaction(user_input, gemini_response):
    log_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "gemini_response": gemini_response
    }

    log_file = "interaction_log.json"

    try:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = []

        data.append(log_data)

        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"[Log Error] {e}")
