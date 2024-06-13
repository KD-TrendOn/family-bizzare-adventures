from fastapi import APIRouter

from .storys.views import router as story_router

router = APIRouter()
router.include_router(router=story_router, prefix="/storys")
