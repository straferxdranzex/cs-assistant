from uuid import UUID, uuid4
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Ticket(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="open")

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tickets")
    messages = relationship(
        "Message", back_populates="ticket", cascade="all, delete-orphan"
    )


class Message(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    content = Column(String, nullable=False)
    is_ai = Column(Boolean, default=False)

    # Foreign keys
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("ticket.id"), nullable=False)

    # Relationships
    ticket = relationship("Ticket", back_populates="messages")
