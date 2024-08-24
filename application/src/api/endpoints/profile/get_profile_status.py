from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Request, HTTPException, status
from application.src.orm import ProfileORM
from application.src.schemas import ProfileItemInit

router = APIRouter()


@router.get("/status")
async def get_profile_status(request: Request) -> ProfileItemInit:
    """
    API endpoint to retrieve the status of the user's profile.

    This endpoint checks if the user's profile exists. If it does, the profile ID is returned.
    If no profile is found, a 404 Not Found error is raised.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.

    Returns:
        ProfileItemInit: A response model containing the ID of the user's profile.

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

    # Return the profile ID in the response model
    return ProfileItemInit(
        id=profile.id
    )
