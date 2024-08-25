from fastapi import APIRouter

from .generate_lesson import router as generate_lesson
from .submit_lesson import router as submit_lesson

router = APIRouter()

router.include_router(generate_lesson)
router.include_router(submit_lesson)
