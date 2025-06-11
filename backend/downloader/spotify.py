"""Helpers for interacting with Spotify playlists via ``spotdl``."""

from typing import List
from spotdl import Spotdl


def fetch_spotify_playlist(playlist_url: str) -> List[str]:
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
    songs = spotdl_handler.search([playlist_url])
    return [song.title for song in songs]


class SpotifyDownloader:
    """Wrapper around :func:`fetch_spotify_playlist`."""

    def download(self, url: str) -> List[str]:
        """Fetch tracks from ``url`` using spotdl."""

        return fetch_spotify_playlist(url)
