import enum
from typing import Union, List, Dict, Optional
from pydantic import BaseModel, field_validator


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
    context: Optional[str]
    options: List[str]
    answer: int
    level: str


class FillInTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.fill_in
    question: str
    options: List[str]
    answer: int
    level: str


class MultipleChoiceTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.multiple_choice
    question: str
    options: List[str]
    answer: int
    level: str


class MatchingTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.matching
    question: str
    pairs: List[Dict[str, str]]
    level: str


class RearrangeTask(BaseModel):
    type: TaskTypeEnum = TaskTypeEnum.rearrange
    question: str
    sentence: str
    words: List[str]
    level: str


class Task(BaseModel):
    task: Union[TranslationTask, FillInTask, MultipleChoiceTask, MatchingTask, RearrangeTask]

    @field_validator('task', mode='before')
    def validate_task(cls, v):
        match v.get('type'):
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
                raise ValueError(f"Unsupported task type: {v.get('type')}")


class Lesson(BaseModel):
    tasks: List[Task]
