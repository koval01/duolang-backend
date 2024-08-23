import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import PkBase
from .profile import Profile


class TaskTypeEnum(str, enum.Enum):
    translation = "translation"
    fill_in = "fill-in"
    multiple_choice = "multiple-choice"
    matching = "matching"
    rearrange = "rearrange"


class Lesson(PkBase):
    __tablename__ = "lesson"

    profile_id = Column(ForeignKey('profile.id'), nullable=False)
    profile = relationship("Profile", back_populates="lessons")
    tasks = relationship("Task", back_populates="lesson", cascade="all, delete-orphan")
    result = Column(JSON, nullable=True)  # Stores user's results (e.g., {"task_id": {"correct": True}})
    total_score = Column(Integer, default=0)

    @hybrid_property
    def score(self):
        return self.total_score

    @score.expression
    def score(cls):
        return cls.total_score

    def update_score(self):
        if self.result:
            self.total_score = sum([1 for task_result in self.result.values() if task_result["correct"]])


class Task(PkBase):
    __tablename__ = "task"

    lesson_id = Column(ForeignKey('lesson.id'), nullable=False)
    lesson = relationship("Lesson", back_populates="tasks")
    type = Column(Enum(TaskTypeEnum), nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=True)  # Stores options for MCQ, fill-in, etc.
    pairs = Column(JSON, nullable=True)  # Stores matching pairs for matching tasks
    sentence = Column(String, nullable=True)  # Stores sentence for rearrange task
    correct_answer = Column(Integer, nullable=True)  # Stores index of correct answer for MCQ, fill-in
    words = Column(JSON, nullable=True)  # Stores words for rearrange task


Profile.lessons = relationship("Lesson", order_by=Lesson.id, back_populates="profile")
