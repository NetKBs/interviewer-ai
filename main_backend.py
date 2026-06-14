from backend.vision import VisionAnalyzer
from backend.audio import AudioAnalyzer
from backend.feedback import FeedbackGenerator

class CIMBackend:
    def __init__(self):
        self.vision = VisionAnalyzer()
        self.audio = AudioAnalyzer()
        self.feedback = FeedbackGenerator()

    def process_interview_session(self, audio_path, frames, job_description, duration):
        """
        Orchestrates the analysis of an interview session.
        """
        # 1. Vision Analysis (Batch process frames)
        vision_results = []
        for frame in frames:
            res = self.vision.process_frame(frame)
            vision_results.append(res)
        
        # Calculate eye contact percentage
        eye_contact_count = sum(1 for r in vision_results if r.get("eye_contact"))
        eye_contact_percent = (eye_contact_count / len(frames)) * 100 if frames else 0

        # 2. Audio Analysis
        transcription = self.audio.transcribe_audio(audio_path)
        wpm = self.audio.calculate_wpm(transcription, duration)

        # 3. Feedback Generation
        feedback = self.feedback.generate_feedback(transcription, job_description)

        return {
            "eye_contact_percent": round(eye_contact_percent, 2),
            "wpm": wpm,
            "transcription": transcription,
            "feedback": feedback.model_dump()
        }
