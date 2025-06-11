# AllPlatformMusic Downloader

## 🌟 Overview

AllPlatformMusic Downloader is a backend-focused tool that allows users to download music tracks and playlists from multiple platforms (Spotify, YouTube, YouTube Music, SoundCloud, etc.) with high matching accuracy.

Users can upload a `.txt` file listing songs or provide a playlist link, and the system will:

* Search the track across multiple platforms.
* Download the highest-matching version.
* Zip the files and provide the download.
* Clean up the temporary data after download.

## Quickstart

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

To handle background tasks you need a running Redis instance. Configure
`CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in your environment and start a
Celery worker:

```bash
celery -A backend.tasks worker --loglevel=info
```


---

## 🚀 Project Goals

* Automatically find and download music tracks from the best matching platform.
* Cross-platform support for playlist conversion (e.g., Spotify playlists downloaded from YouTube Music).
* Support remix/fallback logic: if original track is not found, try SoundCloud or other platforms.
* Temporary file storage, zip bundling, and auto-deletion logic after user download.

---

## 📒 Use Cases

### 1. Download from `.txt` File

User uploads a `.txt` file with each line containing a song name.

* System searches each track across platforms.
* Downloads best match into `temp/` directory.
* After all downloads are complete, creates a `.zip` file.
* Serves the `.zip` to user and deletes all temporary files.

### 2. Download from Playlist Link

User provides a playlist link (e.g., from Spotify):

* System fetches all tracks from the playlist.
* Each track is matched with YouTube Music / SoundCloud alternatives.
* Download and zip process proceeds similarly.

---

## 🔄 Retry & Error Handling

* Each download task includes a `retry_limit` (e.g., 3 tries per track).
* Errors are logged.
* If a track fails to download after retries, it is recorded in a `not_downloaded.txt` file inside the user's temporary directory.
* All tasks are handled asynchronously for performance (via asyncio or Celery+Redis).

---

## 🔧 Tech Stack

### Backend

* **Language**: Python
* **Framework**: FastAPI (recommended)
* **Libraries**:

  * `yt-dlp` for YouTube / YouTube Music
  * `spotDL` for Spotify playlist conversion
  * `scdl` or direct API for SoundCloud
* **Process**:

  * Download files to `/temp`
  * Generate `.zip`
  * Serve zip and delete all files

## ⚙️ Setup

1. Clone the repository.
2. Install Python 3.10+.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server (example):
   ```bash
   uvicorn backend.main:app --reload
   ```

### Running Tests

After installing the dependencies you can run the test suite with
`pytest`:

```bash
pytest
```

### Frontend

The repository contains a [`create-next-app`](https://nextjs.org/) project in
`frontend/`. It exposes pages for user login, playlist upload and task progress
which communicate with the FastAPI backend.

To run the development server:

```bash
cd frontend
npm install
npm run dev
```

The pages use the backend running on `http://localhost:8000` for authentication
and download status APIs.


---

## 🤔 Planned Features

* Genre-based folder grouping
* Remix filtering logic
* Language selector (TR/EN)
* Email zip delivery (optional)
* Platform fallback prioritization

---

## 📂 Suggested Folder Structure

```bash
allplatformmusic/
├── backend/
│   ├── main.py
│   ├── downloader/
│   │   ├── youtube.py
│   │   ├── spotify.py
│   │   ├── soundcloud.py
│   └── utils/
│       ├── zipper.py
│       └── matcher.py
├── temp/
├── output/
├── requirements.txt
└── README.md
```

### Downloader Modules

The downloader package exposes convenience functions:

* `download_youtube_track(url: str, output_dir: Path) -> Path`
* `fetch_spotify_playlist(playlist_url: str) -> List[str]`
* `download_soundcloud_track(url: str, output_dir: Path) -> Path`

These helpers are thin wrappers around ``yt-dlp``, ``spotdl`` and ``scdl``
respectively.

---

## 👋 Contributing
Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, coding style and pull request guidelines. Focus areas include:
* Match scoring improvement
* Platform API integration
* Download performance optimization

---

## 📢 License

This project is licensed under the [MIT License](LICENSE).
