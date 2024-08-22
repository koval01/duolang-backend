from fastapi import APIRouter, Depends

from application.src.api.endpoints import profile, lesson
from application.src.dependency.auth import auth_dependency

from application.src.api.endpoints import healthz

api_router = APIRouter()

api_router.include_router(
    lesson.router, prefix="/lesson", tags=["Lesson"], dependencies=[Depends(auth_dependency)])
api_router.include_router(
    profile.router, prefix="/profile", tags=["Profile"], dependencies=[Depends(auth_dependency)])

api_router.include_router(healthz.router)
