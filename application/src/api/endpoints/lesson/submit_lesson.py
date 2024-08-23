from typing import Dict

from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from application.src.models import Lesson, Profile
from application.src.schemas import Lesson as LessonSchema, TaskTypeEnum

router = APIRouter()


@router.post("/submit", response_model=Dict[str, int])
async def submit_lesson_responses(request: Request, responses: LessonSchema) -> JSONResponse:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Fetch the user's profile using Telegram ID
    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile does not exist")

    # Fetch the lesson
    lesson = await db.session.get(Lesson, responses.lesson_id)
    if not lesson or lesson.profile_id != profile.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    # Check responses and calculate points
    lesson_result = {}
    for response in responses.responses:
        task = next((t for t in lesson.tasks if t.id == response.task_id), None)
        if not task:
            continue
        correct = False
        if task.type == TaskTypeEnum.multiple_choice or task.type == TaskTypeEnum.fill_in:
            correct = task.correct_answer == response.user_answer
        elif task.type == TaskTypeEnum.rearrange:
            correct = task.words == response.user_answer
        elif task.type == TaskTypeEnum.matching:
            correct = task.pairs == response.user_answer

        lesson_result[task.id] = {"correct": correct}

    # Update lesson result and profile score
    lesson.result = lesson_result
    lesson.update_score()
    profile.total_score += lesson.total_score

    await db.session.commit()

    return JSONResponse({"score": lesson.total_score})
