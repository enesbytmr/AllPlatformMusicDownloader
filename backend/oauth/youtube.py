from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import os

from ..auth.router import get_current_user
from ..auth import models
from ..auth.database import get_db

router = APIRouter()

CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "dummy")
REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "http://localhost/callback/youtube")
AUTH_URL = (
    "https://accounts.google.com/o/oauth2/auth?client_id="
    f"{CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
)

@router.get("/connect/youtube")
def connect_youtube(current_user: models.User = Depends(get_current_user)):
    return RedirectResponse(AUTH_URL)

@router.get("/callback/youtube")
def youtube_callback(code: str, db = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    token = f"youtube_token_{code}"
    current_user.youtube_token = token
    db.add(current_user)
    db.commit()
    return {"access_token": token}
