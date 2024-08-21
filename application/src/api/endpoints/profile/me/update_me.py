from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, HTTPException, Request, status
from fastapi_async_sqlalchemy import db

from pydantic import ValidationError

from sqlalchemy import select, update

from application.src.models.profile import Profile
from application.src.schemas.profile import ProfileItemUpdate, ProfileItemDisplay

router = APIRouter()


@router.put("/")
async def update_me(request: Request, _: ProfileItemUpdate) -> ProfileItemDisplay:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate request body
    try:
        body = ProfileItemUpdate(**await request.json())
    except ValidationError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")

    query = (
        update(Profile)
        .where(Profile.telegram == web_app_init_data.user.id)
        .values(**body.model_dump(exclude_none=True))
        .returning(Profile)
    )
    result = await db.session.execute(query)
    updated_profile = result.scalars().first()
    await db.session.commit()

    return ProfileItemDisplay(
        id=updated_profile.id,
        telegram=updated_profile.telegram,
        createdAt=updated_profile.createdAt,
        displayName=updated_profile.displayName,
        visible=updated_profile.visible,
        avatar=updated_profile.avatar
    )
