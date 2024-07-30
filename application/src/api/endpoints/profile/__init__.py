from fastapi import APIRouter

from .get_profiles import router as get_profiles_router
from .init_profile import router as init_profile_router
from .get_profile_status import router as get_profile_status_router
from .get_profile_by_id import router as get_profile_by_id_router

from .me import router as me_router

router = APIRouter()

router.include_router(get_profiles_router, tags=["profile"])
router.include_router(init_profile_router, tags=["profile"])
router.include_router(get_profile_status_router, tags=["profile"])
router.include_router(get_profile_by_id_router, tags=["profile"])

router.include_router(
    me_router, prefix="/me", tags=["me"])
