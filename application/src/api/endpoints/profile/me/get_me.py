from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, HTTPException, Request, status
from fastapi_async_sqlalchemy import db

from sqlalchemy import select

from .....models.profile import Profile
from .....schemas.profile import ProfileItemDisplay

router = APIRouter()


@router.get("/")
async def get_me(request: Request) -> ProfileItemDisplay:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")

    return ProfileItemDisplay(
        id=profile.id,
        telegram=profile.telegram,
        createdAt=profile.createdAt,
        displayName=profile.displayName,
        visible=profile.visible,
        avatar=profile.avatar
    )
