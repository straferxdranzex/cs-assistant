from uuid import UUID, uuid4
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships
    tickets = relationship("Ticket", back_populates="user")
