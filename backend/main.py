"""FastAPI server exposing music download endpoints."""

import asyncio
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse

from .downloader.youtube import download_youtube_track
from .downloader.spotify import fetch_spotify_playlist
from .utils.zipper import zip_temp_directory

app = FastAPI()


async def _download_tracks(tracks: list[str], temp_dir: Path) -> None:
    """Download all ``tracks`` into ``temp_dir`` concurrently."""

    async def _download(track: str) -> None:
        query = f"ytsearch1:{track}"
        await asyncio.to_thread(download_youtube_track, query, temp_dir)

    tasks = [asyncio.create_task(_download(t)) for t in tracks]
    await asyncio.gather(*tasks)


@app.post("/download/text")
async def download_from_text(file: UploadFile = File(...)):
    """Accept a .txt file of tracks, download them and return a zip."""

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    data = await file.read()
    lines = [line.strip() for line in data.decode().splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="File is empty")

    temp_dir = Path(tempfile.mkdtemp(dir="temp"))

    await _download_tracks(lines, temp_dir)
    zip_path = await asyncio.to_thread(zip_temp_directory, temp_dir)

    return FileResponse(zip_path, filename=zip_path.name)


@app.post("/download/playlist")
async def download_from_playlist(link: str = Form(...)):
    """Fetch playlist ``link`` and return downloaded zip."""

    tracks = await asyncio.to_thread(fetch_spotify_playlist, link)
    if not tracks:
        raise HTTPException(status_code=404, detail="No tracks found")

    temp_dir = Path(tempfile.mkdtemp(dir="temp"))

    await _download_tracks(tracks, temp_dir)
    zip_path = await asyncio.to_thread(zip_temp_directory, temp_dir)

    return FileResponse(zip_path, filename=zip_path.name)


@app.get("/")
async def root():
    return {"message": "Hello, World"}
