from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, UUID4


class MessageBase(BaseModel):
    content: str
    is_ai: bool = False


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: UUID4
    created_at: datetime
    ticket_id: UUID4

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    title: str
    description: str
    status: str = "open"


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Ticket(TicketBase):
    id: UUID4
    created_at: datetime
    user_id: UUID4
    messages: List[Message] = []

    class Config:
        from_attributes = True
