from fastapi import APIRouter, Depends

from ..api.endpoints import profile
from ..dependency.auth import auth_dependency

api_router = APIRouter()

api_router.include_router(
    profile.router, prefix="/profile", tags=["profile"], dependencies=[Depends(auth_dependency)])
