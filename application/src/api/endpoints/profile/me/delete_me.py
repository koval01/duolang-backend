from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Request
from application.src.orm import ProfileORM
from application.src.schemas import ResultBody

router = APIRouter()


@router.delete("/")
async def delete_me(request: Request) -> ResultBody:
    """
    API endpoint to delete the current user's profile.

    This endpoint deletes the profile associated with the current user.
    It returns a success status indicating whether the deletion was successful.

    Args:
        request (Request): The incoming request object containing WebApp initialization data.

    Returns:
        ResultBody: A response model indicating the success of the deletion operation.
    """
    # Extract WebApp initialization data from the request's state
    web_app_init_data: WebAppInitData = request.state.web_app_init_data

    # Create an instance of ProfileORM using the initialization data
    _orm = ProfileORM(web_app_init_data)

    # Attempt to delete the user's profile
    result = await _orm.delete_user()

    # Return the result of the deletion operation
    return ResultBody(
        success=result
    )
