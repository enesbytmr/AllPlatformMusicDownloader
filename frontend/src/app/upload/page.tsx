'use client'
import { useState, useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../AuthContext'

export default function Upload() {
  const [link, setLink] = useState('')
  const router = useRouter()
  const { token } = useContext(AuthContext)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const resp = await fetch('http://localhost:8000/download/playlist', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: new URLSearchParams({ link })
    })
    if (resp.ok) {
      const data = await resp.json()
      const tasks = JSON.parse(localStorage.getItem('tasks') || '[]')
      localStorage.setItem('tasks', JSON.stringify([data.task_id, ...tasks]))
      router.push(`/progress/${data.task_id}`)
    } else {
      alert('Upload failed')
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Upload Playlist</h1>
      <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxWidth: '400px' }}>
        <input value={link} onChange={e => setLink(e.target.value)} placeholder="Spotify playlist link" required />
        <button type="submit">Start Download</button>
      </form>
    </main>
  )
}
