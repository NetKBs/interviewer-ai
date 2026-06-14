# CUDI Interview Mastery (CIM)

CIM is an AI-powered interview simulator that provides real-time feedback on eye contact, speech rate (WPM), and technical content using the STAR method.

## 🚀 Tech Stack
- **Frontend:** Streamlit + Streamlit WebRTC
- **Vision:** MediaPipe (Local)
- **Transcription:** Google Gemini 1.5 Flash API
- **Feedback:** Deepseek API (via OpenAI SDK)
- **Data Validation:** Pydantic v2

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/))
- A Deepseek API Key ([Get one here](https://platform.deepseek.com/))

### 2. Environment Setup
```bash
# The environment is already created in the workspace
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
# Edit .env with your keys
```

## 🧪 Testing

### Offline Logic Tests
These tests verify math and data structures without calling external APIs:
```bash
./venv/bin/python3 test_backend.py
```

### Live Integration Test (Requires API Keys)
To test the real connection to Gemini and Deepseek, you can run the integration test script:
```bash
./venv/bin/python3 integration_test.py
```

### End-to-End Sample Test
To test with real video (.mp4) and audio (.mp3) samples:
1. Place `test_video.mp4` and `test_audio.mp3` in the `samples/` folder.
2. Run:
```bash
./venv/bin/python3 e2e_test.py
```

## 📂 Project Structure
- `backend/`: Core logic for vision, audio, and AI feedback.
- `main_backend.py`: Orchestrator for the interview session.
- `venv/`: Python virtual environment.
- `requirements.txt`: Project dependencies.
