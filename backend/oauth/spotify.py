from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from ..auth.router import get_current_user
from ..auth import models
from ..auth.database import get_db

router = APIRouter()

AUTH_URL = "https://accounts.spotify.com/authorize?client_id=dummy&response_type=code&redirect_uri=http://localhost/callback/spotify"

@router.get("/connect/spotify")
def connect_spotify(current_user: models.User = Depends(get_current_user)):
    return RedirectResponse(AUTH_URL)

@router.get("/callback/spotify")
def spotify_callback(code: str, db = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    token = f"spotify_token_{code}"
    current_user.spotify_token = token
    db.add(current_user)
    db.commit()
    return {"access_token": token}
