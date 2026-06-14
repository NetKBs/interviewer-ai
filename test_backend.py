import unittest
from backend.audio import AudioAnalyzer
from backend.feedback import FeedbackGenerator, InterviewFeedback

class TestBackend(unittest.TestCase):
    def test_wpm_calculation(self):
        analyzer = AudioAnalyzer()
        text = "This is a test of the words per minute calculation logic."
        # 11 words: This(1) is(2) a(3) test(4) of(5) the(6) words(7) per(8) minute(9) calculation(10) logic(11)
        duration = 10 # 10 seconds = 1/6 minute
        # 11 / (1/6) = 66 WPM
        wpm = analyzer.calculate_wpm(text, duration)
        self.assertEqual(wpm, 66.0)

    def test_feedback_model(self):
        # Verify Pydantic validation
        data = {
            "puntaje_global": 85,
            "analisis_star": {
                "situation": "Team conflict",
                "task": "Resolve it",
                "action": "Talked to them",
                "result": "Harmony"
            },
            "mejoras_comunicacion": ["Use better vocabulary"]
        }
        feedback = InterviewFeedback(**data)
        self.assertEqual(feedback.puntaje_global, 85)

if __name__ == "__main__":
    unittest.main()
