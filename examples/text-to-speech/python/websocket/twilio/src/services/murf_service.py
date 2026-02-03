import json
import asyncio
import websockets
from typing import Callable, Optional
from src.config import MURF_API_KEY, MURF_WS_URL, MURF_MODEL, SAMPLE_RATE, AUDIO_FORMAT, VOICE_CONFIG


class MurfService:
    def __init__(
        self,
        on_open: Optional[Callable[[], None]] = None,
        on_audio: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_close: Optional[Callable[[int, str], None]] = None
    ):
        self.on_open = on_open
        self.on_audio = on_audio
        self.on_error = on_error
        self.on_close = on_close
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self._receive_task: Optional[asyncio.Task] = None

    async def connect(self):
        """Establish WebSocket connection to Murf TTS API."""
        url = f"{MURF_WS_URL}?api_key={MURF_API_KEY}&model={MURF_MODEL}&sample_rate={SAMPLE_RATE}&format={AUDIO_FORMAT}"

        try:
            self.ws = await websockets.connect(url)
            print("Connected to Murf WebSocket")

            if self.on_open:
                self.on_open()

            # Start receiving messages in background
            self._receive_task = asyncio.create_task(self._receive_messages())

        except Exception as e:
            print(f"Failed to connect to Murf: {e}")
            if self.on_error:
                self.on_error(e)

    async def _receive_messages(self):
        """Background task to receive messages from Murf."""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    audio_data = data.get("audio")

                    if audio_data:
                        print(f"Received audio chunk from Murf ({len(audio_data)} bytes)")
                        if self.on_audio:
                            self.on_audio(audio_data)
                    elif data.get("error"):
                        print(f"Murf error: {data.get('error')}")
                        if self.on_error:
                            self.on_error(Exception(data.get("error")))

                except json.JSONDecodeError as e:
                    print(f"Failed to parse Murf message: {e}")

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Murf WebSocket closed: code={e.code}, reason={e.reason}")
            if self.on_close:
                self.on_close(e.code, e.reason)
        except Exception as e:
            print(f"Error receiving Murf messages: {e}")
            if self.on_error:
                self.on_error(e)

    async def send_text(self, text: str, context_id: Optional[str] = None):
        """Send text to Murf for TTS synthesis."""
        if not self.ws:
            print("Cannot send text: Murf WebSocket not connected")
            return

        message = {
            "text": text,
            "format": AUDIO_FORMAT,
            "voice_config": {
                "voiceId": VOICE_CONFIG["voice_id"],
                "style": VOICE_CONFIG["style"]
            },
            "end": True  # Signal that text input is complete
        }

        if context_id:
            message["context_id"] = context_id

        try:
            await self.ws.send(json.dumps(message))
            print(f"Sent text to Murf: {text}")
        except Exception as e:
            print(f"Failed to send text to Murf: {e}")
            if self.on_error:
                self.on_error(e)

    async def disconnect(self):
        """Close the WebSocket connection."""
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        if self.ws:
            await self.ws.close()
            self.ws = None
            print("Disconnected from Murf WebSocket")
