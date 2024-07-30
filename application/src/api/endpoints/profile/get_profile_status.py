from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Request
from fastapi_async_sqlalchemy import db

from sqlalchemy import select

from ....models.profile import Profile
from ....schemas.profile import ProfileItem

router = APIRouter()


@router.get("/status")
async def get_profile_status(request: Request) -> ProfileItem:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()

    return ProfileItem(
        id=profile.id
    )
