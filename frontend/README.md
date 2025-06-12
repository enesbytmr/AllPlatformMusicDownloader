# Frontend Setup

This folder contains the Next.js interface for AllPlatformMusic Downloader.

## 1. Install dependencies

```bash
npm install
```

## 2. Configure the API base URL

Create a `.env.local` file and set the backend address:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

The app stores the JWT token in `localStorage` under the key `token` after a successful login.

## 3. Start the development server

```bash
npm run dev
```

Open <http://localhost:3000> in your browser to use the app.

## Available Pages

- **/login** – user login page that obtains a JWT and stores it in `localStorage`.
- **/upload** – form to submit a Spotify playlist link. Requires a logged-in user.
- **/progress/[taskId]** – displays download progress and provides the resulting zip file.
