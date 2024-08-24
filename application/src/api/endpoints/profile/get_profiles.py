from typing import List
from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Request, HTTPException, status
from application.src.schemas import ProfileItemDisplay
from application.src.orm.profile import ProfileORM

router = APIRouter()


@router.get("/")
async def get_profiles(request: Request) -> List[ProfileItemDisplay]:
    """
    API endpoint to retrieve all user profiles.

    This endpoint returns a list of profiles if the requester has admin privileges.
    Only an admin user can fetch all profiles.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.

    Returns:
        List[ProfileItem]: A list of profiles, each represented by a ProfileItem schema.

    Raises:
        HTTPException: If the requester is not an admin (403 Forbidden).
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Fetch the profile of the current user
    profile = await _orm.fetch_user()

    # Check if the current user is an admin
    if not ProfileORM.is_admin(profile):
        # Raise a 403 Forbidden error if the user is not an admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # Fetch profiles of all users since the current user is an admin
    profiles = await _orm.fetch_user(all_users=True)

    # Return the list of profiles, each represented by a ProfileItem schema
    return [
        ProfileItemDisplay.from_orm(row) for row in profiles
    ]
