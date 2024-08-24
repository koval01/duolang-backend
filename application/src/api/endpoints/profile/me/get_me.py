from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, HTTPException, Request, status

from application.src.orm import ProfileORM
from application.src.schemas import ProfileItemDisplay

router = APIRouter()


@router.get("/")
async def get_me(request: Request) -> ProfileItemDisplay:
    """
    API endpoint to retrieve the current user's profile.

    This endpoint fetches the profile associated with the current user.
    If the profile is not found, a 404 Not Found error is raised.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.

    Returns:
        ProfileItemDisplay: A response model containing the details of the user's profile.

    Raises:
        HTTPException: If the user's profile is not found (404).
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Fetch the user's profile from the database
    profile = await _orm.fetch_user()

    # If the profile does not exist, raise a 404 Not Found error
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")

    # Return the profile details in the response model
    return ProfileItemDisplay.model_validate(profile)
