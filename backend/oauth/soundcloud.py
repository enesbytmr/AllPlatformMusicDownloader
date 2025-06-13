from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import os

from ..auth.router import get_current_user
from ..auth import models
from ..auth.database import get_db

router = APIRouter()

CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID", "dummy")
REDIRECT_URI = os.getenv(
    "SOUNDCLOUD_REDIRECT_URI",
    "http://localhost/callback/soundcloud",
)
AUTH_URL = (
    "https://soundcloud.com/connect?client_id="
    f"{CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
)

@router.get("/connect/soundcloud")
def connect_soundcloud(current_user: models.User = Depends(get_current_user)):
    return RedirectResponse(AUTH_URL)

@router.get("/callback/soundcloud")
def soundcloud_callback(code: str, db = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    token = f"soundcloud_token_{code}"
    current_user.soundcloud_token = token
    db.add(current_user)
    db.commit()
    return {"access_token": token}
