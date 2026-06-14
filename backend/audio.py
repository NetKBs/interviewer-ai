import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AudioAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-flash-latest")

    def transcribe_audio(self, audio_path):
        """
        Transcribes audio using Gemini 1.5 Flash.
        Returns the transcription text and WPM.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Upload the file to Gemini
        audio_file = genai.upload_file(path=audio_path)
        
        # Wait for the file to be processed
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)

        if audio_file.state.name == "FAILED":
            raise Exception("Gemini audio processing failed")

        # Generate transcription
        prompt = "Transcribe the following audio exactly as spoken."
        response = self.model.generate_content([prompt, audio_file])
        
        transcription = response.text
        
        # Cleanup remote file
        genai.delete_file(audio_file.name)
        
        return transcription

    def calculate_wpm(self, text, duration_seconds):
        """
        Calculates Words Per Minute.
        """
        if duration_seconds <= 0 or not text:
            return 0
        
        # Use a more robust word split (remove extra whitespace)
        words = [w for w in text.split() if w.strip()]
        word_count = len(words)
        minutes = duration_seconds / 60
        wpm = word_count / minutes
        
        return round(wpm, 2)
