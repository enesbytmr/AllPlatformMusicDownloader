"""YouTube download utilities using ``yt-dlp``."""

from pathlib import Path
from yt_dlp import YoutubeDL


def download_youtube_track(url: str, output_dir: Path) -> Path:
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

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return Path(filename)


class YouTubeDownloader:
    """Simple wrapper class for YouTube downloads."""

    def download(self, url: str, output_dir: Path) -> Path:
        """Download ``url`` to ``output_dir`` using :func:`download_youtube_track`."""

        return download_youtube_track(url, output_dir)
