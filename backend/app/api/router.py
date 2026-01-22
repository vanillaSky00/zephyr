from fastapi import APIRouter
from app.api.v1.media import router as media_router
from app.api.v1.timeline import router as timeline_router

router = APIRouter(prefix="/v1")
router.include_router(media_router)
router.include_router(timeline_router)
