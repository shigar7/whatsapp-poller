import os
import time
from dotenv import load_dotenv
from whatsapp_sdk.client import WhatsAppClient

load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER") # e.g., 'whatsapp:+14155238886'

def poll_messages():
    """
    Simulates a polling API by checking Twilio message logs every few seconds.
    """
    client = WhatsAppClient(
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_number=TWILIO_FROM_NUMBER
    )
    
    print(f"Starting polling for {TWILIO_FROM_NUMBER}...")
    print("Press Ctrl+C to stop.")

    last_seen_sid = None

    # First run: get the most recent message SID so we don't process old history
    # Filter by 'from_' to only look for messages NOT from the bot itself
    # But since we want messages *from* you, we'll just check the 'from' field manually
    initial_messages = client.client.messages.list(to=TWILIO_FROM_NUMBER, limit=1)
    if initial_messages:
        last_seen_sid = initial_messages[0].sid
        print(f"Initial state set. Last message seen: {last_seen_sid}")

    while True:
        try:
            # Fetch the most recent message sent TO the sandbox
            messages = client.client.messages.list(to=TWILIO_FROM_NUMBER, limit=1)
            
            if messages:
                latest_msg = messages[0]
                
                # Check if this is a new message we haven't processed
                # AND ensure it's NOT an outgoing message (status: 'delivered', 'sent', etc.)
                # Incoming messages usually have a direction of 'inbound'
                if latest_msg.sid != last_seen_sid and latest_msg.direction == 'inbound':
                    sender_id = latest_msg.from_
                    body = latest_msg.body
                    
                    print(f"\n[NEW MESSAGE] From {sender_id}: {body}")
                    
                    # Echo back
                    reply_body = f"Poller received: '{body}'"
                    client.send_text_message(to=sender_id, body=reply_body)
                    print(f"Replied to {sender_id}")
                    
                    # Update the tracker
                    last_seen_sid = latest_msg.sid
            
            # Wait 3 seconds before checking again to avoid rate limits
            time.sleep(3)
            
        except Exception as e:
            print(f"Error during polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    poll_messages()
