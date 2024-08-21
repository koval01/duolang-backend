from fastapi import APIRouter, Depends

from application.src.api.endpoints import profile
from application.src.dependency.auth import auth_dependency

api_router = APIRouter()

api_router.include_router(
    profile.router, prefix="/profile", tags=["profile"], dependencies=[Depends(auth_dependency)])
