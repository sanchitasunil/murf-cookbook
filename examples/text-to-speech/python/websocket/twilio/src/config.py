import os
from dotenv import load_dotenv

load_dotenv()

# Murf configuration
MURF_API_KEY = os.getenv("MURF_API_KEY")
MURF_WS_URL = "wss://global.api.murf.ai/v1/speech/stream-input"
MURF_MODEL = "FALCON"
SAMPLE_RATE = 8000
AUDIO_FORMAT = "ULAW"

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
TWILIO_API_KEY_SECRET = os.getenv("TWILIO_API_KEY_SECRET")

# Server configuration
PORT = int(os.getenv("PORT", 3000))
NGROK_URL = os.getenv("NGROK_URL")

# Test call configuration
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

# Voice configuration
VOICE_CONFIG = {
    "voice_id": "en-US-matthew",
    "style": "Conversational"
}

GREETING_TEXT = "Hi, This is a greeting from the Murf Twilio Demo. Goodbye!"
