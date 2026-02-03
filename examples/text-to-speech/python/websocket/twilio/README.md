# Murf Twilio Integration (Python)

A Python implementation of real-time text-to-speech integration between Murf AI and Twilio for phone calls.

## Overview

This application bridges Murf AI's TTS engine with Twilio's phone calling platform, enabling real-time audio streaming over phone calls.

### Call Flow

1. **Incoming Call** → Twilio receives a phone call and hits the `/voice` webhook
2. **TwiML Response** → Server responds with TwiML instructing Twilio to establish a WebSocket connection
3. **WebSocket Handshake** → Twilio connects via WebSocket to `/streams`
4. **Murf Connection** → Application connects to Murf's WebSocket TTS API
5. **Greeting Delivery** → Once both connections are ready, a greeting is sent to Murf for synthesis
6. **Audio Streaming** → Murf synthesizes text and streams back audio
7. **Twilio Playback** → Audio is forwarded to Twilio to play on the active call

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- Murf AI API key
- Twilio account with:
  - Account SID
  - API Key SID and Secret
  - Phone number capable of making/receiving calls
- ngrok (for local development)

## Installation

1. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository and navigate to the project:

```bash
cd murf-twilio-py
```

3. Install dependencies:

```bash
uv sync
```

This will automatically create a virtual environment and install all dependencies.

4. Copy the environment example and configure:

```bash
cp .env.example .env
```

5. Edit `.env` with your credentials:

```
MURF_API_KEY=your_murf_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_API_KEY_SID=your_twilio_api_key_sid
TWILIO_API_KEY_SECRET=your_twilio_api_key_secret
NGROK_URL=https://your-ngrok-url.ngrok.io
FROM_NUMBER=+1234567890
TO_NUMBER=+0987654321
```

## Usage

### Start the Server

```bash
uv run python -m src.server
```

The server will start on port 3000 (or the port specified in `PORT` environment variable).

### Expose with ngrok

In a separate terminal:

```bash
ngrok http 3000
```

Update your `.env` file with the ngrok URL.

### Make a Test Call

```bash
uv run python test_call.py
```

## Configuration

| Variable | Description |
|----------|-------------|
| `MURF_API_KEY` | Your Murf AI API key |
| `TWILIO_ACCOUNT_SID` | Twilio account identifier |
| `TWILIO_API_KEY_SID` | Twilio API key SID |
| `TWILIO_API_KEY_SECRET` | Twilio API key secret |
| `PORT` | Server port (default: 3000) |
| `NGROK_URL` | Public URL for webhook exposure |
| `FROM_NUMBER` | Outbound caller phone number (E.164 format) |
| `TO_NUMBER` | Target phone number (E.164 format) |

## API Endpoints

### POST /voice

Webhook endpoint for incoming Twilio calls. Returns TwiML to establish WebSocket connection.

### WebSocket /streams

Bidirectional WebSocket connection for real-time audio streaming between Twilio and Murf.

## Technical Details

- **Audio Format**: ULAW (mu-law compression)
- **Sample Rate**: 8000 Hz (telephony standard)
- **Voice**: Matthew with Conversational style
- **Model**: FALCON
