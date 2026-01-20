# Murf-Twilio Integration

Real-time text-to-speech integration between Murf AI and Twilio using WebSockets. This example demonstrates how to stream AI-generated speech directly to phone calls.

## Prerequisites

- Node.js installed
- Murf API key
- Twilio account with phone number
- Twilio API key

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
MURF_API_KEY=your_murf_api_key_here

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_API_KEY_SID=your_twilio_api_key_sid
TWILIO_API_KEY_SECRET=your_twilio_api_key_secret

NGROK_URL=https://your-ngrok-url.ngrok.io
PORT=3000

FROM_NUMBER=+1234567890
TO_NUMBER=+0987654321
```

### 3. Start the Server

```bash
npm start
```

### 4. Expose Webhook (for local testing)

```bash
ngrok http 3000
```

Update `NGROK_URL` in `.env` with the ngrok URL.

### 5. Make a Test Call

```bash
npm test
```

## Architecture

- **Express Server**: Handles incoming Twilio webhooks
- **WebSocket Bridge**: Connects Twilio Media Streams with Murf TTS

## How It Works

1. Incoming call triggers `/voice` webhook
2. Twilio establishes WebSocket connection to `/streams`
3. Server connects to Murf TTS WebSocket
4. Text is sent to Murf and synthesized audio is streamed back to caller
5. Audio is forwarded directly to Twilio in real-time
