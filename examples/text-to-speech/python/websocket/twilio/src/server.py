import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import Response
from src.services.twilio_service import TwilioService
from src.config import PORT

app = FastAPI()


@app.post("/voice")
async def voice_webhook(request: Request):
    """Handle incoming Twilio voice webhook."""
    print("Incoming call received")

    # Get the host from headers for WebSocket URL
    host = request.headers.get("host", f"localhost:{PORT}")

    # Build TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://{host}/streams" />
    </Connect>
</Response>"""

    return Response(content=twiml, media_type="text/xml")


@app.websocket("/streams")
async def websocket_streams(websocket: WebSocket):
    """Handle Twilio media stream WebSocket connection."""
    await websocket.accept()
    print("Twilio WebSocket connected")

    # Create and initialize Twilio service
    twilio_service = TwilioService(websocket)
    await twilio_service.initialize()

    try:
        while True:
            message = await websocket.receive_text()
            await twilio_service.handle_message(message)
    except WebSocketDisconnect:
        print("Twilio WebSocket disconnected")
        await twilio_service.handle_close()
    except Exception as e:
        print(f"WebSocket error: {e}")
        await twilio_service.handle_close()


def main():
    """Start the server."""
    print(f"Server starting on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
