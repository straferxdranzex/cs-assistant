from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Common columns
    created_at = DateTime(timezone=True, server_default=func.now())
    updated_at = DateTime(timezone=True, onupdate=func.now())
