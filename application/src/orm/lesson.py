from fastapi_async_sqlalchemy import db

from application.src.models import Profile, Lesson
from application.src.schemas import Lesson as LessonSchema


class LessonORM:
    def __init__(self, profile: Profile) -> None:
        self.profile = profile

    async def add_lesson(self, lesson: LessonSchema) -> Lesson:
        new_lesson = Lesson(profile_id=self.profile.id, **lesson.model_dump())
        db.session.add(new_lesson)
        await db.session.commit()
        await db.session.refresh(new_lesson)

        return new_lesson
