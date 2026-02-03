import json
import asyncio
from typing import Optional
from fastapi import WebSocket
from src.services.murf_service import MurfService
from src.config import GREETING_TEXT


class TwilioService:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.stream_sid: Optional[str] = None
        self.murf_ready = False
        self.greeting_sent = False

        # Initialize Murf service with callbacks
        self.murf_service = MurfService(
            on_open=self._on_murf_open,
            on_audio=self._on_murf_audio,
            on_error=self._on_murf_error,
            on_close=self._on_murf_close
        )

        # Event loop reference for thread-safe operations
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def initialize(self):
        """Initialize the service and connect to Murf."""
        self._loop = asyncio.get_event_loop()
        await self.murf_service.connect()

    def _on_murf_open(self):
        """Called when Murf WebSocket connection opens."""
        print("Murf connection ready")
        self.murf_ready = True
        # Schedule greeting check on the event loop
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self._send_greeting_if_ready(),
                self._loop
            )

    def _on_murf_audio(self, base64_audio: str):
        """Called when Murf sends audio data."""
        print(f"Forwarding audio to Twilio ({len(base64_audio)} bytes)")
        # Schedule sending audio to Twilio on the event loop
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self._send_audio_to_twilio(base64_audio),
                self._loop
            )

    def _on_murf_error(self, error: Exception):
        """Called when Murf WebSocket encounters an error."""
        print(f"Murf error: {error}")

    def _on_murf_close(self, code: int, reason: str):
        """Called when Murf WebSocket closes."""
        print(f"Murf connection closed: code={code}, reason={reason}")
        self.murf_ready = False

    async def _send_greeting_if_ready(self):
        """Send greeting if both Murf and Twilio are ready."""
        if self.murf_ready and self.stream_sid and not self.greeting_sent:
            self.greeting_sent = True
            print("Both connections ready, sending greeting...")
            await self.murf_service.send_text(GREETING_TEXT)

    async def _send_audio_to_twilio(self, base64_audio: str):
        """Send audio data to Twilio WebSocket."""
        if not self.stream_sid:
            print("Cannot send audio: no stream SID")
            return

        message = {
            "event": "media",
            "streamSid": self.stream_sid,
            "media": {
                "payload": base64_audio
            }
        }

        try:
            await self.websocket.send_json(message)
            print(f"Sent audio chunk to Twilio")
        except Exception as e:
            print(f"Failed to send audio to Twilio: {e}")

    async def handle_message(self, message: str):
        """Handle incoming message from Twilio."""
        try:
            data = json.loads(message)
            event = data.get("event")

            if event == "connected":
                print("Twilio media stream connected")

            elif event == "start":
                self.stream_sid = data.get("streamSid")
                print(f"Twilio stream started: {self.stream_sid}")
                await self._send_greeting_if_ready()

            elif event == "media":
                # Incoming audio from caller - not processing in this demo
                pass

            elif event == "stop":
                print("Twilio stream stopped")
                await self.handle_close()

        except json.JSONDecodeError as e:
            print(f"Failed to parse Twilio message: {e}")

    async def handle_close(self):
        """Handle WebSocket close."""
        print("Twilio connection closing, disconnecting Murf...")
        await self.murf_service.disconnect()
