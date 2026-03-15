import os
from groq import Groq
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

import speech_recognition as sr
import tempfile
from pydub import AudioSegment

load_dotenv()

# -------- API CLIENTS --------
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# -------- AI RESPONSE --------
def get_ai_response(messages):

    system_prompt = {
        "role": "system",
        "content": "You are VoxAI, a helpful voice assistant. Always respond clearly in English."
    }

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[system_prompt] + messages
    )

    return response.choices[0].message.content


# -------- TEXT TO SPEECH --------
def text_to_speech(text):

    try:

        text = text[:300]

        response = eleven_client.text_to_speech.convert(
            voice_id="r3nowsTGyuxutyTiwyBy",
            model_id="eleven_multilingual_v2",
            text=text
        )

        file_path = "response.mp3"

        with open(file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        return file_path

    except Exception as e:
        print("TTS ERROR:", e)
        return None

# -------- SPEECH TO TEXT --------
def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    try:
        # save webm audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            webm_path = f.name

        # convert webm → wav
        wav_path = webm_path.replace(".webm", ".wav")

        audio = AudioSegment.from_file(webm_path)
        audio.export(wav_path, format="wav")

        # speech recognition
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        return text

    except Exception as e:
        print("Speech error:", e)
        return "Sorry, I couldn't understand the audio."