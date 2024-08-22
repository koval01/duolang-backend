from fastapi import Request, HTTPException, Header
from aiogram.utils.web_app import safe_parse_webapp_init_data

from application.src.config import settings


async def auth_dependency(
    request: Request,
    init_data: str = Header(..., alias="X-InitData")
):
    if not init_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        web_app_init_data = safe_parse_webapp_init_data(
            token=settings.BOT_TOKEN, init_data=init_data
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add parsed data to request state for use in endpoints
    request.state.web_app_init_data = web_app_init_data
