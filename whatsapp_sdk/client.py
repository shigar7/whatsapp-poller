import os
from twilio.rest import Client
from typing import Optional

class WhatsAppClient:
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initializes the Twilio WhatsApp client.
        :param account_sid: Your Twilio Account SID.
        :param auth_token: Your Twilio Auth Token.
        :param from_number: Your Twilio Sandbox number (e.g., 'whatsapp:+14155238886').
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_text_message(self, to: str, body: str) -> str:
        """
        Sends a WhatsApp message to a specific number.
        :param to: The recipient's number (e.g., 'whatsapp:+1234567890').
        :param body: The message text.
        :return: The message SID.
        """
        # Ensure numbers are prefixed with 'whatsapp:'
        if not to.startswith("whatsapp:"):
            to = f"whatsapp:{to}"
        if not self.from_number.startswith("whatsapp:"):
            self.from_number = f"whatsapp:{self.from_number}"

        message = self.client.messages.create(
            from_=self.from_number,
            body=body,
            to=to
        )
        return message.sid
