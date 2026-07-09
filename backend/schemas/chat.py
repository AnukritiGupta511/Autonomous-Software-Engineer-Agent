import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ChatMessageCreate(BaseModel):
    content: str

class ChatMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    metadata_json: dict | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatCreate(BaseModel):
    repository_id: str | None = None
    title: str | None = None

class ChatResponse(BaseModel):
    id: str
    title: str
    repository_id: str | None = None
    messages: list[ChatMessageResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
