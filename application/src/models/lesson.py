import enum

from sqlalchemy import Column, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID

from .base import PkBase


class TaskTypeEnum(str, enum.Enum):
    translation = "translation"
    fill_in = "fill-in"
    multiple_choice = "multiple-choice"
    matching = "matching"
    rearrange = "rearrange"


class Lesson(PkBase):
    """Lesson model"""
    __tablename__ = 'lesson'

    user_id = Column(UUID(as_uuid=True), ForeignKey('profile.id'), nullable=False)
    score = Column(Float, default=0.0)  # Total score for the lesson

    user = relationship("Profile", back_populates="lessons")
    tasks = relationship("Task", back_populates="lesson")  # Define relationship here

    @hybrid_property
    def grade(self):
        if not self.tasks:
            return 0.0

        correct_tasks = sum(1 for task in self.tasks if task.correct)
        return correct_tasks / len(self.tasks) * 100

    def calculate_grade(self):
        """Calculate and update the lesson grade."""
        self.score = self.grade


class Task(PkBase):
    """Base Task model"""
    __tablename__ = 'task'

    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lesson.id'), nullable=False)
    type = Column(Enum(TaskTypeEnum), nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    correct = Column(Boolean, nullable=False, default=False)

    lesson = relationship("Lesson", back_populates="tasks")
