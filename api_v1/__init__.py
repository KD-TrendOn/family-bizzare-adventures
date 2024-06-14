from fastapi import APIRouter

from .storys.views import router as story_router
from .nodes.views import router as node_router
router = APIRouter()
router.include_router(router=story_router, prefix="/storys")
router.include_router(router=node_router, prefix="/nodes")