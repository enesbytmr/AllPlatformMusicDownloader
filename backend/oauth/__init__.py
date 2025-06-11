from fastapi import APIRouter

from . import spotify, youtube, soundcloud

router = APIRouter()
router.include_router(spotify.router)
router.include_router(youtube.router)
router.include_router(soundcloud.router)

__all__ = ["router"]
