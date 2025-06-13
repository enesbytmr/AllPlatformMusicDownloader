'use client'
import { useState, useEffect, useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../AuthContext'

export default function Dashboard() {
  const { token, loaded } = useContext(AuthContext)
  const router = useRouter()
  const [link, setLink] = useState('')
  const [tasks, setTasks] = useState<string[]>([])
  const [statuses, setStatuses] = useState<Record<string, string>>({})

  useEffect(() => {
    if (loaded && !token) {
      router.push('/login')
    } else if (token) {
      const stored = JSON.parse(localStorage.getItem('tasks') || '[]')
      setTasks(stored)
    }
  }, [loaded, token])

  useEffect(() => {
    if (!tasks.length) return
    const timer = setInterval(() => {
      tasks.forEach(async id => {
        const resp = await fetch(`http://localhost:8000/status/${id}`)
        if (resp.ok) {
          const data = await resp.json()
          setStatuses(s => ({ ...s, [id]: data.status }))
        }
      })
    }, 2000)
    return () => clearInterval(timer)
  }, [tasks])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const resp = await fetch('http://localhost:8000/download/playlist', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: new URLSearchParams({ link })
    })
    if (resp.ok) {
      const data = await resp.json()
      const newTasks = [data.task_id, ...tasks]
      setTasks(newTasks)
      localStorage.setItem('tasks', JSON.stringify(newTasks))
      router.push(`/progress/${data.task_id}`)
    } else {
      alert('Upload failed')
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxWidth: '400px' }}>
        <input value={link} onChange={e => setLink(e.target.value)} placeholder="Spotify playlist link" required />
        <button type="submit">Start Download</button>
      </form>
      {tasks.length > 0 && (
        <>
          <h2>Recent Tasks</h2>
          <ul>
            {tasks.map(id => (
              <li key={id}>
                <a href={`/downloads/${id}`}>{id}</a> – {statuses[id] || 'PENDING'}
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  )
}
