# WhatsApp SDK for Meta Cloud API

A lightweight Python library for interacting with the official Meta WhatsApp Cloud API. This SDK simplifies sending messages and handling incoming webhooks.

## Project Structure

- `whatsapp_sdk/`: Core library package.
  - `client.py`: `WhatsAppClient` for sending messages and marking them as read.
  - `webhook.py`: `WebhookHandler` for verification and parsing incoming messages.
  - `models.py`: Pydantic models for structured data validation.
- `examples/`: Implementation examples.
  - `test_wrapper.py`: A FastAPI-based example showing how to use the SDK.
- `requirements.txt`: Project dependencies.
- `.env.example`: Template for required environment variables.

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your Meta Cloud API credentials.
   ```bash
   cp .env.example .env
   ```

3. **Run the Test Wrapper:**
   The test wrapper provides a local server that can receive WhatsApp messages and echo them back.
   ```bash
   python -m examples.test_wrapper
   ```

## WhatsApp Cloud API Setup (Manual Steps)

To use this library, you must:
1.  **Create a Meta Developer App:** Go to [developers.facebook.com](https://developers.facebook.com/) and create a "Business" app.
2.  **Add WhatsApp:** Add the "WhatsApp" product to your app.
3.  **Get Credentials:**
    - `WHATSAPP_PHONE_ID`: Found in the WhatsApp "Getting Started" or "Configuration" tab.
    - `WHATSAPP_TOKEN`: Generate a "Permanent Token" in your System User settings (Meta Business Suite).
    - `WEBHOOK_VERIFY_TOKEN`: A string of your choice that you'll also enter in the Meta Webhook configuration.
4.  **Configure Webhook:**
    - Use a tool like `ngrok` to expose your local port (e.g., `ngrok http 8000`).
    - In Meta Developer Portal -> WhatsApp -> Configuration:
        - Callback URL: `https://your-ngrok-url.com/webhook`
        - Verify Token: Your `WEBHOOK_VERIFY_TOKEN`.
    - Subscribe to `messages` in the Webhook fields.
