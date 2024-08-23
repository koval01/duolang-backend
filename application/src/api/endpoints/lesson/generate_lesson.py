from typing import Literal

from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Request, HTTPException, status
from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from pydantic import ValidationError, BaseModel

from application.src.gemini import Gemini
from application.src.models import Lesson, Profile
from application.src.schemas import Lesson as LessonSchema

router = APIRouter()


class InitRequestBody(BaseModel):
    course: Literal["de-ru"]


@router.post("/generate", response_model=LessonSchema)
async def generate_lesson(request: Request, _: InitRequestBody) -> LessonSchema:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate request body
    try:
        body = InitRequestBody(**await request.json())
    except ValidationError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    # Fetch the user's profile using Telegram ID
    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile does not exist")

    # Generate lesson using Gemini (mocked for example)
    generated_lesson: Lesson = Gemini().execute(body.course)

    # Store lesson in the database
    new_lesson = LessonSchema(profile_id=profile.id, tasks=generated_lesson.tasks)
    db.session.add(new_lesson)
    await db.session.commit()

    for task in new_lesson.tasks:
        del task.answer

    return new_lesson
