from fastapi import APIRouter

from .get_profiles import router as get_profiles
from .init_profile import router as init_profile
from .get_profile_status import router as get_profile_status
from .get_profile_by_id import router as get_profile_by_id

from .me import router as me_router

router = APIRouter()

router.include_router(get_profiles)
router.include_router(init_profile)
router.include_router(get_profile_status)
router.include_router(get_profile_by_id)

router.include_router(
    me_router, prefix="/me", tags=["me"])
