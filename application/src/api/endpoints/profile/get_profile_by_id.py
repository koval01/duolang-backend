from uuid import UUID
from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, HTTPException, status, Request
from application.src.orm import ProfileORM
from application.src.schemas import ProfileItemDisplay

router = APIRouter()


@router.get("/{profile_id}")
async def get_profile_by_id(request: Request, profile_id: UUID) -> ProfileItemDisplay:
    """
    API endpoint to retrieve a user profile by its ID.

    This endpoint fetches the profile associated with the provided `profile_id`.
    If the profile is not found, a 404 Not Found error is raised.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.
        profile_id (UUID): The UUID of the profile to be retrieved.

    Returns:
        ProfileItemDisplay: A response model containing the details of the retrieved profile.

    Raises:
        HTTPException: If the profile is not found (404).
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Fetch the profile from the database using the provided profile ID
    profile = await _orm.fetch_user(by_id=profile_id)

    # If the profile does not exist, raise a 404 Not Found error
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # Return the profile details in the response model
    return ProfileItemDisplay.model_validate(profile)
