from pydantic import BaseModel
from typing import List, Dict, Union
from typing_extensions import Literal


class BaseTaskAnswer(BaseModel):
    task_type: Literal["translation", "fill-in", "multiple-choice", "matching", "rearrange"]


class TranslationAnswer(BaseTaskAnswer):
    task_type: Literal["translation"] = "translation"


class FillInAnswer(BaseTaskAnswer):
    task_type: Literal["fill-in"] = "fill-in"
    answer: int


class MultipleChoiceAnswer(BaseTaskAnswer):
    task_type: Literal["multiple-choice"] = "multiple-choice"
    answer: int


class MatchingAnswer(BaseTaskAnswer):
    task_type: Literal["matching"] = "matching"
    pairs: List[Dict[str, str]]


class RearrangeAnswer(BaseTaskAnswer):
    task_type: Literal["rearrange"] = "rearrange"
    sentence: str


class UserAnswers(BaseModel):
    answers: List[Union[TranslationAnswer, FillInAnswer, MultipleChoiceAnswer, MatchingAnswer, RearrangeAnswer]]
