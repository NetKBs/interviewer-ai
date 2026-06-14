import cv2
import os
import time
from dotenv import load_dotenv
from main_backend import CIMBackend

load_dotenv()

def run_e2e_test(video_path, audio_path, job_desc):
    """
    Runs a full end-to-end test of the CIM Backend.
    """
    print("--- Starting End-to-End Backend Test ---")
    
    # 1. Check if files exist
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return

    # 2. Extract frames from video for Vision Analysis
    print(f"📦 Extracting frames from {video_path}...")
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Process 1 frame per second to save computation during test
        if count % int(fps) == 0:
            frames.append(frame)
        count += 1
    cap.release()
    print(f"✅ Extracted {len(frames)} frames.")

    # 3. Calculate duration
    duration = count / fps
    print(f"🕒 Estimated Duration: {duration:.2f} seconds")

    # 4. Run Orchestrator
    print("\n🚀 Running CIM Backend Orchestrator...")
    print("(This involves uploading to Gemini and calling Deepseek, please wait...)")
    
    try:
        backend = CIMBackend()
        results = backend.process_interview_session(
            audio_path=audio_path,
            frames=frames,
            job_description=job_desc,
            duration=duration
        )

        # 5. Display Results
        print("\n" + "="*50)
        print("🏆 TEST RESULTS")
        print("="*50)
        print(f"👁️ Eye Contact: {results['eye_contact_percent']}%")
        print(f"🗣️ Speech Rate: {results['wpm']} WPM")
        print(f"📝 Transcription: \"{results['transcription'][:100]}...\"")
        print("\n🤖 AI FEEDBACK:")
        print(f"⭐ Global Score: {results['feedback']['puntaje_global']}/100")
        print(f"✅ STAR Analysis: {results['feedback']['analisis_star']}")
        print(f"💬 Communication Tips: {results['feedback']['mejoras_comunicacion']}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Error during orchestrator execution: {e}")

if __name__ == "__main__":
    # YOU CAN CHANGE THESE PATHS TO YOUR REAL FILES
    SAMPLE_VIDEO = "sample/test_video.mp4"
    SAMPLE_AUDIO = "sample/test_audio.mp3"
    SAMPLE_JD = "Senior Python Developer with experience in AI and Cloud."

    # Instructions for the user
    if not os.path.exists("sample"):
        os.makedirs("sample")
        print("📁 Created 'sample/' directory.")
        print("Please place a 'test_video.mp4' and 'test_audio.mp3' inside it.")
    else:
        run_e2e_test(SAMPLE_VIDEO, SAMPLE_AUDIO, SAMPLE_JD)
