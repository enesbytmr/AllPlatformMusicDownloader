import os
import asyncio
import shutil
import tempfile
from pathlib import Path

from celery import Celery

from .downloader.youtube import download_youtube_track
from .utils.zipper import zip_temp_directory

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
celery.conf.task_always_eager = (
    os.getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true"
)


def _record_failure(track: str, user_id: int) -> None:
    """Append ``track`` to ``temp/{user_id}/not_downloaded.txt``."""

    fail_log = Path("temp") / str(user_id) / "not_downloaded.txt"
    fail_log.parent.mkdir(parents=True, exist_ok=True)
    with fail_log.open("a") as f:
        f.write(track + "\n")


def _cleanup(zip_path: Path, temp_dir: Path, user_id: int) -> None:
    """Delete created files and directories for ``user_id``."""

    if zip_path.exists():
        zip_path.unlink()
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)

    fail_log = Path("temp") / str(user_id) / "not_downloaded.txt"
    if fail_log.exists():
        fail_log.unlink()

    user_dir = Path("temp") / str(user_id)
    if user_dir.exists():
        shutil.rmtree(user_dir, ignore_errors=True)


async def _download_tracks_async(tracks: list[str], temp_dir: Path, user_id: int) -> None:
    """Download all ``tracks`` into ``temp_dir`` concurrently."""

    fail_log = Path("temp") / str(user_id) / "not_downloaded.txt"

    async def _download(track: str) -> None:
        query = f"ytsearch1:{track}"
        try:
            await asyncio.to_thread(
                download_youtube_track, query, temp_dir, fail_log=fail_log
            )
        except Exception:
            await asyncio.to_thread(_record_failure, track, user_id)

    tasks = [asyncio.create_task(_download(t)) for t in tracks]
    await asyncio.gather(*tasks)


@celery.task(bind=True)
def download_tracks(self, tracks: list[str], user_id: int) -> dict:
    """Celery task that downloads ``tracks`` for ``user_id`` and cleans up."""

    self.update_state(meta={"user_id": user_id})

    user_dir = Path("temp") / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(dir=user_dir))

    asyncio.run(_download_tracks_async(tracks, temp_dir, user_id))
    zip_path = zip_temp_directory(temp_dir)
    return {"zip_path": str(zip_path), "user_id": user_id}
