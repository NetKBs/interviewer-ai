import os
from dotenv import load_dotenv
from backend.feedback import FeedbackGenerator
from backend.audio import AudioAnalyzer

load_dotenv()

def test_deepseek_connection():
    print("Testing Deepseek API...")
    try:
        gen = FeedbackGenerator()
        feedback = gen.generate_feedback(
            transcription="I worked at a big tech company where I led a team to migrate a legacy system to microservices. It was hard but we finished on time.",
            job_description="Senior Software Engineer with experience in microservices."
        )
        print("✅ Deepseek Connection Successful!")
        print(f"Sample Score: {feedback.puntaje_global}")
    except Exception as e:
        print(f"❌ Deepseek Error: {e}")

def test_gemini_connection():
    # Note: This requires a real audio file to test transcription.
    # For now, we just check if the model initializes.
    print("\nTesting Gemini API Initialization...")
    try:
        analyzer = AudioAnalyzer()
        print("✅ Gemini Model Initialized Successfully!")
        print("(To test full transcription, provide a sample .wav file in integration_test.py)")
    except Exception as e:
        print(f"❌ Gemini Error: {e}")

if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: API Keys not found in .env file.")
        print("Please copy .env.example to .env and fill in your keys.")
    else:
        test_deepseek_connection()
        test_gemini_connection()
