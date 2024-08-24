from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import ValidationError
from application.src.orm import ProfileORM
from application.src.schemas import ProfileItemUpdate, ProfileItemDisplay

router = APIRouter()


@router.put("/")
async def update_me(request: Request, _: ProfileItemUpdate) -> ProfileItemDisplay:
    """
    API endpoint to update the current user's profile.

    This endpoint allows the current user to update their profile information.
    The updated profile is returned upon successful update.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.
        _ (ProfileItemUpdate): Placeholder for the request body, validated later.

    Returns:
        ProfileItemDisplay: A response model containing the updated profile details.

    Raises:
        HTTPException:
            - If the request body is invalid (400).
            - If the user's profile is not found (404).
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Validate request body
    try:
        body = ProfileItemUpdate(**await request.json())
    except ValidationError as _:
        # Raise a 400 Bad Request error if the request body is not valid
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Fetch the user's profile from the database
    profile = await _orm.fetch_user()

    # If the profile does not exist, raise a 404 Not Found error
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")

    # Update the user's profile with the new data
    updated_profile = await _orm.update_user(body)

    # Return the updated profile details in the response model
    return ProfileItemDisplay.from_orm(updated_profile)
