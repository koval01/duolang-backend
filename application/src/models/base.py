import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class PkBase:
    """Base model with default columns."""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    updatedAt = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    createdAt = Column(DateTime, server_default=func.now())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
