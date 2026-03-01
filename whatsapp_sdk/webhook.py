from typing import Dict, Any, Optional

class WebhookHandler:
    def __init__(self):
        """Twilio webhooks are simpler, we just need to parse the form data."""
        pass

    def parse_incoming_message(self, form_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extracts sender and message body from Twilio's incoming webhook.
        :param form_data: The POST form data from Twilio (FastAPI Request.form()).
        :return: A dictionary containing 'from', 'body', and 'sid'.
        """
        return {
            "from": form_data.get("From", ""),
            "body": form_data.get("Body", ""),
            "sid": form_data.get("MessageSid", "")
        }
