import enum
from typing import Union, List, Dict
from pydantic import BaseModel, field_validator, model_validator, RootModel

from application.src.models import Lesson as LessonModel


class TaskTypeEnum(str, enum.Enum):
    translation = "translation"
    fill_in = "fill-in"
    multiple_choice = "multiple-choice"
    matching = "matching"
    rearrange = "rearrange"


class TranslationTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.translation
    question: str
    direction: str
    context: str | None
    options: List[str]
    answer: int
    level: str

    @field_validator('direction')
    def validate_direction(cls, v):
        allowed_directions = ["de-ru"]
        if v not in allowed_directions:
            raise ValueError(f"Invalid direction: {v}. Allowed values are: {allowed_directions}")
        return v

    @field_validator('level')
    def validate_level(cls, v):
        allowed_levels = ["A1", "A2"]
        if v not in allowed_levels:
            raise ValueError(f"Invalid level: {v}. Allowed values are: {allowed_levels}")
        return v

    @field_validator('options')
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("There must be at least two options.")
        if len(set(v)) != len(v):
            raise ValueError("All options must be unique.")
        return v

    @field_validator('answer')
    def validate_answer(cls, v, values):
        options = values.data.get('options', [])
        if v < 0 or v >= len(options):
            raise ValueError("Answer index must be within the range of the options list.")
        return v


class FillInTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.fill_in
    question: str
    options: List[str]
    answer: int
    level: str

    @field_validator('options')
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("There must be at least two options.")
        if len(set(v)) != len(v):
            raise ValueError("All options must be unique.")
        return v

    @field_validator('answer')
    def validate_answer(cls, v, values):
        options = values.data.get('options', [])
        if v < 0 or v >= len(options):
            raise ValueError("Answer index must be within the range of the options list.")
        return v

    @field_validator('level')
    def validate_level(cls, v):
        allowed_levels = ["A1", "A2"]
        if v not in allowed_levels:
            raise ValueError(f"Invalid level: {v}. Allowed values are: {allowed_levels}")
        return v


class MultipleChoiceTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.multiple_choice
    question: str
    options: List[str]
    answer: int
    level: str

    @field_validator('options')
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("There must be at least two options.")
        if len(set(v)) != len(v):
            raise ValueError("All options must be unique.")
        return v

    @field_validator('answer')
    def validate_answer(cls, v, values):
        options = values.data.get('options', [])
        if v < 0 or v >= len(options):
            raise ValueError("Answer index must be within the range of the options list.")
        return v

    @field_validator('level')
    def validate_level(cls, v):
        allowed_levels = ["A1", "A2"]
        if v not in allowed_levels:
            raise ValueError(f"Invalid level: {v}. Allowed values are: {allowed_levels}")
        return v


class MatchingTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.matching
    question: str
    pairs: List[Dict[str, str]]
    level: str

    @field_validator('pairs')
    def validate_pairs(cls, v):
        if not v or len(v) < 2:
            raise ValueError("There must be at least two pairs to match.")
        return v

    @field_validator('level')
    def validate_level(cls, v):
        allowed_levels = ["A1", "A2"]
        if v not in allowed_levels:
            raise ValueError(f"Invalid level: {v}. Allowed values are: {allowed_levels}")
        return v


class RearrangeTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.rearrange
    question: str
    sentence: str
    words: List[str]
    level: str

    @field_validator('words')
    def validate_words(cls, v):
        if len(v) < 2:
            raise ValueError("There must be at least two words to rearrange.")
        if len(set(v)) != len(v):
            raise ValueError("All words must be unique.")
        return v

    @field_validator('level')
    def validate_level(cls, v):
        allowed_levels = ["A1", "A2"]
        if v not in allowed_levels:
            raise ValueError(f"Invalid level: {v}. Allowed values are: {allowed_levels}")
        return v


class Task(RootModel):
    root: Union[TranslationTask, FillInTask, MultipleChoiceTask, MatchingTask, RearrangeTask]

    @classmethod
    def validate_task(cls, v):
        task_type = v.get('type')
        match task_type:
            case TaskTypeEnum.translation:
                return TranslationTask(**v)
            case TaskTypeEnum.fill_in:
                return FillInTask(**v)
            case TaskTypeEnum.multiple_choice:
                return MultipleChoiceTask(**v)
            case TaskTypeEnum.matching:
                return MatchingTask(**v)
            case TaskTypeEnum.rearrange:
                return RearrangeTask(**v)
            case _:
                raise ValueError(f"Unsupported task type: {task_type}")


class Lesson(BaseModel):
    tasks: List[Task]

    @model_validator(mode="before")
    def validate_tasks(cls, values):
        if isinstance(values, LessonModel):
            tasks = values.tasks
        else:
            tasks = values.get('tasks', [])
        if not tasks:
            raise ValueError("There must be at least one task in a lesson.")
        return values

    class Config:
        from_attributes = True
