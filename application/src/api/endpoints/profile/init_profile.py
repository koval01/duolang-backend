from aiogram.utils.web_app import WebAppInitData

from fastapi import APIRouter, Request, HTTPException, status
from fastapi_async_sqlalchemy import db

from pydantic import ValidationError, BaseModel
from sqlalchemy import select

from ....models.profile import Profile
from ....schemas.profile import ProfileItemCreate, ProfileItemInit

router = APIRouter()


class InitRequestBody(BaseModel):
    displayName: str


@router.post("/init", response_model=ProfileItemInit)
async def init_profile(request: Request, _: InitRequestBody) -> ProfileItemInit:
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate request body
    try:
        body = InitRequestBody(**await request.json())
    except ValidationError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    # Check if profile already exists
    query = select(Profile).where(Profile.telegram == web_app_init_data.user.id)
    result = await db.session.execute(query)
    profile = result.scalars().first()
    if profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    # Create a new profile
    new_profile = ProfileItemCreate(
        displayName=body.displayName,
        telegram=web_app_init_data.user.id,
    )
    new_profile = Profile(**new_profile.model_dump())
    db.session.add(new_profile)
    await db.session.commit()
    await db.session.refresh(new_profile)

    return ProfileItemInit(
        id=new_profile.id
    )
