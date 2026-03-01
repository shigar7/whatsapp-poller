from pydantic import BaseModel, Field
from typing import List, Optional, Any

# --- Outgoing Message Models ---

class Text(BaseModel):
    body: str
    preview_url: bool = False

class Message(BaseModel):
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    to: str
    type: str = "text"
    text: Optional[Text] = None

# --- Incoming Webhook Models (Meta's nested structure) ---

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class IncomingText(BaseModel):
    body: str

class IncomingMessage(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    text: Optional[IncomingText] = None
    type: str

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[IncomingMessage]] = None

class Change(BaseModel):
    value: Value
    field: str

class Entry(BaseModel):
    id: str
    changes: List[Change]

class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]
