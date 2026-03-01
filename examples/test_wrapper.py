import os
import uvicorn
from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv

from whatsapp_sdk.client import WhatsAppClient
from whatsapp_sdk.webhook import WebhookHandler

load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER") # e.g., 'whatsapp:+14155238886'

app = FastAPI(title="Twilio WhatsApp SDK Test Wrapper")

client = WhatsAppClient(
    account_sid=TWILIO_ACCOUNT_SID,
    auth_token=TWILIO_AUTH_TOKEN,
    from_number=TWILIO_FROM_NUMBER
)
webhook_handler = WebhookHandler()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Receives incoming WhatsApp messages from Twilio.
    Note: Twilio sends data as form-encoded, not JSON.
    """
    form_data = await request.form()
    message_data = webhook_handler.parse_incoming_message(dict(form_data))

    sender_id = message_data.get("from")
    body = message_data.get("body")

    print(f"Received from {sender_id}: {body}")

    # Echo back
    if sender_id and body:
        reply_body = f"Twilio SDK received: '{body}'"
        client.send_text_message(to=sender_id, body=reply_body)
        print(f"Replied to {sender_id}")

    return {"status": "success"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
