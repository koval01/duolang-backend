from typing import Literal

from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Request, HTTPException, status
from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from pydantic import ValidationError, BaseModel

from application.src.gemini import Gemini
from application.src.models import Profile, Lesson, Task
from application.src.schemas import Lesson as LessonSchema, LessonResponse

router = APIRouter()


class InitRequestBody(BaseModel):
    course: Literal["de-ru"]


@router.post("/generate", response_model=LessonSchema)
async def generate_lesson(request: Request, _: InitRequestBody) -> LessonResponse:
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

    # Check if there are any incomplete lessons for the same course
    existing_lesson_query = select(Lesson).where(
        Lesson.profile_id == profile.id,
        Lesson.course == body.course,
        Lesson.completed == False
    )
    existing_lesson_result = await db.session.execute(existing_lesson_query)
    existing_lesson = existing_lesson_result.scalars().first()
    # if existing_lesson:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is an incomplete lesson for this course")

    # Generate lesson using the neural network
    generated_lesson: LessonSchema = Gemini().execute(body.course)

    # Save the lesson to the database
    new_lesson = Lesson(
        profile_id=profile.id,
        course=body.course,
        completed=False,
        tasks=[Task(**task.model_dump()) for task in generated_lesson.tasks]
    )

    db.session.add(new_lesson)
    await db.session.commit()
    await db.session.refresh(new_lesson)

    return LessonResponse(tasks=generated_lesson.tasks)
