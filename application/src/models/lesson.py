from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import PkBase


class Lesson(PkBase):
    __tablename__ = 'lesson'

    profile_id = Column(UUID(as_uuid=True), ForeignKey('profile.id'), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    tasks = Column(JSON, nullable=False)

    # Relationship with Profile
    profile = relationship('Profile', back_populates='lessons')
