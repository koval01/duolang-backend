from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Request, HTTPException, status
from pydantic import ValidationError, BaseModel
from application.src.orm import ProfileORM
from application.src.schemas import ProfileItemInit

router = APIRouter()


class InitRequestBody(BaseModel):
    """
    Pydantic model for validating the request body schema.

    Attributes:
        displayName (str): The display name of the user for the new profile.
    """
    displayName: str


@router.post("/init", response_model=ProfileItemInit)
async def init_profile(request: Request, _: InitRequestBody) -> ProfileItemInit:
    """
    API endpoint to initialize a new user profile.

    Args:
        request (Request): The incoming request object.
        _: (InitRequestBody): The request body containing the display name.

    Returns:
        ProfileItemInit: A response model containing the ID of the initialized profile.

    Raises:
        HTTPException: If the request body is invalid (400) or if the profile already exists (409).
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate the incoming request body
    try:
        body = InitRequestBody(**await request.json())
    except ValidationError as _:
        # Raise a 400 Bad Request error if the request body is not valid
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Check if a profile already exists for the user
    profile = await _orm.exists()
    if profile:
        # Raise a 409 Conflict error if the profile already exists
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    # Create a new profile with the provided display name and return the profile ID
    profile_id = await _orm.init_user(body.displayName)

    # Return the profile ID in the response model
    return ProfileItemInit(
        id=profile_id
    )
