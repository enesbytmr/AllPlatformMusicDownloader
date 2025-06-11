"""FastAPI server exposing music download endpoints."""

import asyncio
from pathlib import Path

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    HTTPException,
    Depends,
    BackgroundTasks,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .auth.router import router as auth_router, get_current_user
from .auth import models as auth_models
from .auth.database import engine, get_db
from .oauth import router as oauth_router
from .billing import router as billing_router, check_quota

from .downloader.spotify import fetch_spotify_playlist
from .tasks import celery, download_tracks
from .tasks import _cleanup

FAIL_LOG = Path("not_downloaded.txt")

app = FastAPI()
auth_models.Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(oauth_router)
app.include_router(billing_router)


@app.post("/download/text")
async def download_from_text(
    file: UploadFile = File(...),
    current_user: auth_models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Accept a .txt file of tracks and start async download."""

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    data = await file.read()
    lines = [line.strip() for line in data.decode().splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="File is empty")

    check_quota(current_user, db, amount=len(lines))
    user_dir = Path("temp") / str(current_user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    task = download_tracks.delay(lines, current_user.id)
    return {"task_id": task.id}


@app.post("/download/playlist")
async def download_from_playlist(
    link: str = Form(...),
    current_user: auth_models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Fetch playlist ``link`` and start async download."""

    tracks = await asyncio.to_thread(fetch_spotify_playlist, link)
    if not tracks:
        raise HTTPException(status_code=404, detail="No tracks found")

    check_quota(current_user, db, amount=len(tracks))
    user_dir = Path("temp") / str(current_user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    task = download_tracks.delay(tracks, current_user.id)
    return {"task_id": task.id}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    """Return Celery task status."""
    result = celery.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status}


@app.post("/cancel/{task_id}")
def cancel_task(task_id: str):
    """Cancel a running task."""
    result = celery.AsyncResult(task_id)
    result.revoke(terminate=True)
    return {"task_id": task_id, "status": "REVOKED"}


@app.get("/download/file/{task_id}")
def serve_file(
    task_id: str,
    background_tasks: BackgroundTasks,
    current_user: auth_models.User = Depends(get_current_user),
):
    """Return the zipped file for ``task_id`` and clean up."""

    result = celery.AsyncResult(task_id)
    if not result.ready():
        raise HTTPException(status_code=202, detail="Task not completed")

    zip_path = Path(result.result)
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    temp_dir = zip_path.with_suffix("")
    background_tasks.add_task(_cleanup, zip_path, temp_dir, current_user.id)
    return FileResponse(zip_path, filename=zip_path.name, media_type="application/zip")


@app.get("/")
async def root():
    return {"message": "Hello, World"}
