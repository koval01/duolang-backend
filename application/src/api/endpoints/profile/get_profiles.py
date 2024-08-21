from typing import List

from fastapi import APIRouter
from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from application.src.models.profile import Profile
from application.src.schemas.profile import ProfileItem

router = APIRouter()


@router.get("/")
async def get_profiles() -> List[ProfileItem]:
    query = select(Profile)
    result = await db.session.execute(query)
    profiles = result.scalars().all()

    return [
        ProfileItem(
            id=row.id,
            createdAt=row.createdAt,
            displayName=row.displayName,
            visible=row.visible,
            avatar=row.avatar,
        ) for row in profiles
    ]
