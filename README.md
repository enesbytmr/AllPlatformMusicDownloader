# AllPlatformMusic Downloader

## 🌟 Overview

AllPlatformMusic Downloader is a backend-focused tool that allows users to download music tracks and playlists from multiple platforms (Spotify, YouTube, YouTube Music, SoundCloud, etc.) with high matching accuracy.

Users can upload a `.txt` file listing songs or provide a playlist link, and the system will:

* Search the track across multiple platforms.
* Download the highest-matching version.
* Zip the files and provide the download.
* Clean up the temporary data after download.

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
* If a track fails to download, it is recorded in a `not_downloaded.txt` file.
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

### Frontend (optional)

* Next.js + Tailwind CSS (planned UI)
* Features:

  * Upload `.txt` or paste playlist link
  * Get download once ready

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

---

## 👋 Contributing

Feel free to fork and suggest improvements! Focus areas include:

* Match scoring improvement
* Platform API integration
* Download performance optimization

---

## 📢 License

MIT License (TBD)
