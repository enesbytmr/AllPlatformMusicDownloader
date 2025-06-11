"""Helpers for interacting with Spotify playlists via ``spotdl``."""

from typing import List, Optional
from pathlib import Path
from spotdl import Spotdl


def fetch_spotify_playlist(
    playlist_url: str, fail_log: Optional[Path] | None = None
) -> List[str]:
    """Return a list of track titles contained in ``playlist_url``.

    Parameters
    ----------
    playlist_url:
        Link to the Spotify playlist.

    Returns
    -------
    List[str]
        The track names found in the playlist.
    """

    spotdl_handler = Spotdl()
    last_exc: Exception | None = None
    for _ in range(3):
        try:
            songs = spotdl_handler.search([playlist_url])
            return [song.title for song in songs]
        except Exception as exc:  # noqa: PERF203
            last_exc = exc

    if fail_log is not None:
        fail_log.parent.mkdir(parents=True, exist_ok=True)
        with fail_log.open("a") as f:
            f.write(playlist_url + "\n")

    if last_exc is not None:
        raise last_exc

    return []


class SpotifyDownloader:
    """Wrapper around :func:`fetch_spotify_playlist`."""

    def download(self, url: str, fail_log: Optional[Path] | None = None) -> List[str]:
        """Fetch tracks from ``url`` using spotdl."""

        return fetch_spotify_playlist(url, fail_log=fail_log)
