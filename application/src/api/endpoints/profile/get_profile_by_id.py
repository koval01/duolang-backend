from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_async_sqlalchemy import db

from sqlalchemy import select

from application.src.models.profile import Profile
from application.src.schemas.profile import ProfileItemDisplay

router = APIRouter()


@router.get("/{profile_id}")
async def get_profile_by_id(profile_id: UUID) -> ProfileItemDisplay:
    query = select(Profile).where(Profile.id == profile_id)
    result = await db.session.execute(query)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return ProfileItemDisplay(
        id=profile.id,
        createdAt=profile.createdAt,
        displayName=profile.displayName,
        visible=profile.visible,
        avatar=profile.avatar
    )
