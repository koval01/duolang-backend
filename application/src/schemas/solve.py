from pydantic import BaseModel
from typing import List, Dict, Union


class TaskResponse(BaseModel):
    task_id: int
    user_answer: Union[int, str, List[str], Dict[str, str]]


class LessonResponse(BaseModel):
    lesson_id: int
    responses: List[TaskResponse]
