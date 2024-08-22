from fastapi import APIRouter

from .get_me import router as get_me
from .update_me import router as update_me
from .delete_me import router as delete_me

router = APIRouter()

router.include_router(get_me)
router.include_router(update_me)
router.include_router(delete_me)
