from twilio.rest import Client
from src.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_API_KEY_SID,
    TWILIO_API_KEY_SECRET,
    NGROK_URL,
    PORT,
    FROM_NUMBER,
    TO_NUMBER
)


def main():
    """Make a test call using Twilio."""
    # Create Twilio client with API key authentication
    client = Client(TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWILIO_ACCOUNT_SID)

    # Determine the webhook URL
    base_url = NGROK_URL if NGROK_URL else f"http://localhost:{PORT}"
    webhook_url = f"{base_url}/voice"

    print(f"Making test call from {FROM_NUMBER} to {TO_NUMBER}")
    print(f"Webhook URL: {webhook_url}")

    try:
        call = client.calls.create(
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            url=webhook_url
        )
        print(f"Call initiated successfully! Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make call: {e}")


if __name__ == "__main__":
    main()
