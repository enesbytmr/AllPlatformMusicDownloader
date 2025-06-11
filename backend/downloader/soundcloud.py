"""SoundCloud download utilities using ``scdl``."""

import subprocess
from pathlib import Path
from typing import Optional


def download_soundcloud_track(
    url: str, output_dir: Path, fail_log: Optional[Path] | None = None
) -> Path:
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

    last_exc: Exception | None = None
    for _ in range(3):
        try:
            subprocess.run(cmd, check=True)
            latest = max(output_dir.glob("*"), key=lambda p: p.stat().st_mtime)
            return latest
        except Exception as exc:  # noqa: PERF203
            last_exc = exc

    if fail_log is not None:
        fail_log.parent.mkdir(parents=True, exist_ok=True)
        with fail_log.open("a") as f:
            f.write(url + "\n")

    if last_exc is not None:
        raise last_exc

    raise RuntimeError("Download failed")


class SoundCloudDownloader:
    """Wrapper class exposing ``download`` for single tracks."""

    def download(
        self, url: str, output_dir: Path, fail_log: Optional[Path] | None = None
    ) -> Path:
        """Download ``url`` using :func:`download_soundcloud_track`."""

        return download_soundcloud_track(url, output_dir, fail_log=fail_log)
