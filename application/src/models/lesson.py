import enum
from typing import Union, List, Dict

from pydantic import BaseModel, field_validator, ValidationError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, ForeignKey, event
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from ..models.base import PkBase


class StudiedLanguageEnum(enum.Enum):
    en = "en"
    de = "de"


class InterfaceLanguageEnum(enum.Enum):
    ru = "ru"
    uk = "uk"


class Task(BaseModel):
    type: str
    sentence: str
    options: Union[List[str], None] = None
    correct_answer: Union[str, Dict[str, str]]
    user_answer: Union[str, Dict[str, str]]

    @field_validator('type')
    def type_must_be_valid(cls, v):
        if v not in [
            'fill_in_the_blank',
            'translate_to_russian',
            'form_question',
            'match_words',
            'negate_sentence',
            'choose_correct_article',
            'translate_to_german',
            'form_sentence'
        ]:
            raise ValueError('Invalid task type')
        return v


class Lesson(PkBase):
    """Lesson model"""
    __tablename__ = 'lesson'

    user_id = Column(UUID(as_uuid=True), ForeignKey('profile.id'), nullable=False)
    language_studied = Column(Enum(StudiedLanguageEnum), nullable=False)
    interface_language = Column(Enum(InterfaceLanguageEnum), nullable=False)
    tasks = Column(JSON, nullable=False)

    user = relationship("Profile", back_populates="lessons")


def validate_tasks(_, __, target):
    tasks = target.tasks
    try:
        [Task(**task) for task in tasks]
    except ValidationError as e:
        raise ValueError(f"Task validation error: {e}")


# Attach the validation listener to the Lesson model
event.listen(Lesson, 'before_insert', validate_tasks)
event.listen(Lesson, 'before_update', validate_tasks)
