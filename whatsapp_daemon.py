import os
import time
from datetime import datetime
from dotenv import load_dotenv
from whatsapp_sdk.client import WhatsAppClient

load_dotenv()

# --- Configuration ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TARGET_NUMBER = "whatsapp:+919930025315"

DATA_DIR = "/home/shigar-docker/data/whatsapp"
INBOX_FILE = os.path.join(DATA_DIR, "inbox.txt")
OUTBOX_DIR = os.path.join(DATA_DIR, "outbox")

def run_daemon():
    client = WhatsAppClient(
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_number=TWILIO_FROM_NUMBER
    )
    
    print(f"Starting WhatsApp Daemon (Polling and Outbox)...")
    print(f"Inbox: {INBOX_FILE}")
    print(f"Outbox: {OUTBOX_DIR}")

    last_seen_sid = None

    # Get the initial state (don't process history)
    try:
        initial_messages = client.client.messages.list(to=TWILIO_FROM_NUMBER, limit=1)
        if initial_messages:
            last_seen_sid = initial_messages[0].sid
            print(f"Initial state set. Last message SID: {last_seen_sid}")
    except Exception as e:
        print(f"Error initializing: {e}")

    while True:
        try:
            # --- 1. Polling for Incoming Messages ---
            # Fetch most recent inbound messages
            messages = client.client.messages.list(to=TWILIO_FROM_NUMBER, limit=5)
            
            # Twilio returns newest first, so we reverse to process in chronological order
            new_messages = []
            for msg in messages:
                if msg.sid == last_seen_sid:
                    break
                if msg.direction == 'inbound':
                    new_messages.append(msg)
            
            # Process new messages in chronological order
            for msg in reversed(new_messages):
                timestamp = msg.date_created.strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp},{msg.body}\n"
                
                with open(INBOX_FILE, "a") as f:
                    f.write(log_entry)
                
                print(f"Received: {msg.body}")
                last_seen_sid = msg.sid

            # --- 2. Checking the Outbox for messages to send ---
            outbox_files = [f for f in os.listdir(OUTBOX_DIR) if os.path.isfile(os.path.join(OUTBOX_DIR, f))]
            
            for filename in outbox_files:
                file_path = os.path.join(OUTBOX_DIR, filename)
                try:
                    with open(file_path, "r") as f:
                        message_body = f.read().strip()
                    
                    if message_body:
                        print(f"Sending message from {filename} to {TARGET_NUMBER}...")
                        client.send_text_message(to=TARGET_NUMBER, body=message_body)
                        print(f"Sent successfully.")
                    
                    # Delete the file after sending
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error processing outbox file {filename}: {e}")

            # Wait 30 seconds as requested
            time.sleep(30)
            
        except Exception as e:
            print(f"Daemon error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    run_daemon()
