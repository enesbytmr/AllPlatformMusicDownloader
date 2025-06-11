"""YouTube download utilities using ``yt-dlp``."""

from pathlib import Path
from typing import Optional
from yt_dlp import YoutubeDL


def download_youtube_track(
    url: str, output_dir: Path, fail_log: Optional[Path] | None = None
) -> Path:
    """Download a single track from YouTube.

    Parameters
    ----------
    url:
        The YouTube video URL.
    output_dir:
        Directory where the audio file will be placed.

    Returns
    -------
    Path
        Path to the downloaded audio file.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "quiet": True,
    }

    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return Path(filename)
        except Exception as exc:  # noqa: PERF203
            last_exc = exc

    if fail_log is not None:
        fail_log.parent.mkdir(parents=True, exist_ok=True)
        with fail_log.open("a") as f:
            f.write(url + "\n")

    if last_exc is not None:
        raise last_exc

    raise RuntimeError("Download failed")


class YouTubeDownloader:
    """Simple wrapper class for YouTube downloads."""

    def download(
        self, url: str, output_dir: Path, fail_log: Optional[Path] | None = None
    ) -> Path:
        """Download ``url`` to ``output_dir`` using :func:`download_youtube_track`."""

        return download_youtube_track(url, output_dir, fail_log=fail_log)
