from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, HTTPException, Request, status
from fastapi_async_sqlalchemy import db

from pydantic import ValidationError

from sqlalchemy import select

from .....models.profile import Profile
from .....schemas.profile import ProfileItemDisplay, ProfileItemUpdate

router = APIRouter()


@router.put("/")
async def update_me(request: Request, _: ProfileItemUpdate) -> ProfileItemDisplay:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate request body
    try:
        ProfileItemUpdate(**await request.json())
    except ValidationError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

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
