"""SoundCloud download utilities using ``scdl``."""

import subprocess
from pathlib import Path


def download_soundcloud_track(url: str, output_dir: Path) -> Path:
    """Download a track from SoundCloud via ``scdl`` command.

    Parameters
    ----------
    url:
        SoundCloud track link.
    output_dir:
        Destination directory for the download.

    Returns
    -------
    Path
        Path of the downloaded file.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "scdl",
        "--onlymp3",
        "--path",
        str(output_dir),
        "-l",
        url,
    ]
    subprocess.run(cmd, check=True)
    latest = max(output_dir.glob("*"), key=lambda p: p.stat().st_mtime)
    return latest


class SoundCloudDownloader:
    """Wrapper class exposing ``download`` for single tracks."""

    def download(self, url: str, output_dir: Path) -> Path:
        """Download ``url`` using :func:`download_soundcloud_track`."""

        return download_soundcloud_track(url, output_dir)
