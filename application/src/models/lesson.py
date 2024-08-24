import enum
import json

from typing import Any

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Enum as SQLAEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, TEXT

from .base import PkBase


class Lesson(PkBase):
    __tablename__ = 'lesson'

    profile_id = Column(UUID(as_uuid=True), ForeignKey('profile.id'), nullable=False)
    score = Column(Integer, default=0, nullable=False)

    # Relationship with Profile
    profile = relationship('Profile', back_populates='lessons')

    # Relationship with Tasks (cascade delete)
    tasks = relationship('Task', back_populates='lesson', cascade='all, delete-orphan')


class TaskTypeEnum(str, enum.Enum):
    translation = "translation"
    fill_in = "fill-in"
    multiple_choice = "multiple-choice"
    matching = "matching"
    rearrange = "rearrange"


class JSONEncodedList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value: Any | None, dialect: Any) -> str | None:
        """Convert Python list or dict to JSON string before storing in the database."""
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value: str | None, dialect: Any) -> Any | None:
        """Convert JSON string from the database back to Python list or dict."""
        if value is None:
            return None
        return json.loads(value)


class Task(PkBase):
    __tablename__ = 'task'

    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lesson.id'), nullable=False)
    type = Column(SQLAEnum(TaskTypeEnum), nullable=False)
    question = Column(String, nullable=False)
    level = Column(String(10), nullable=False)

    # Common fields
    options = Column(JSONEncodedList, nullable=True)  # Storing list of options
    answer = Column(Integer, nullable=True)
    context = Column(String, nullable=True)
    sentence = Column(String, nullable=True)
    pairs = Column(JSONEncodedList, nullable=True)  # Storing list of pairs

    # Relationship with Lesson
    lesson = relationship('Lesson', back_populates='tasks')
