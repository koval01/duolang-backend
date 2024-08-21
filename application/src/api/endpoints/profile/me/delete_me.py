from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Request
from fastapi_async_sqlalchemy import db
from sqlalchemy import delete

from application.src.models.profile import Profile
from application.src.schemas.misc import ResultBody

router = APIRouter()


@router.delete("/")
async def delete_me(request: Request) -> ResultBody:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    query = delete(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    await db.session.commit()

    return ResultBody(
        success=True if result else False
    )
