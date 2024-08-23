from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, UUID, Text, JSON, Enum
from sqlalchemy.orm import relationship

from .base import PkBase
from ..schemas import TaskTypeEnum


class Lesson(PkBase):
    __tablename__ = 'lessons'

    profile_id = Column(UUID(as_uuid=True), ForeignKey('profile.id'), nullable=False)
    course = Column(String(10), nullable=False)
    tasks = relationship('Task', back_populates='lesson', cascade='all, delete-orphan')
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)

    profile = relationship('Profile', back_populates='lessons')


class Task(PkBase):
    __tablename__ = 'tasks'

    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    type = Column(Enum(TaskTypeEnum), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)
    direction = Column(String(5), nullable=True)
    context = Column(String(256), nullable=True)
    answer = Column(Integer)
    pairs = Column(JSON, nullable=True)
    level = Column(String(5), nullable=False)
    sentence = Column(Text, nullable=True)
    words = Column(JSON, nullable=True)

    lesson = relationship('Lesson', back_populates='tasks')
