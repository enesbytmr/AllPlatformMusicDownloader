'use client'
import { useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../AuthContext'
import { API } from '@/api'

export default function Connect() {
  const { token, loaded } = useContext(AuthContext)
  const router = useRouter()

  if (loaded && !token) {
    router.push('/login')
    return null
  }

  const connect = async (service: string) => {
    const resp = await fetch(`${API}/connect/${service}`, {
      headers: { Authorization: `Bearer ${token}` },
      redirect: 'manual'
    })
    const url = resp.headers.get('Location')
    if (url) {
      window.location.href = url
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Connect Accounts</h1>
      <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <li><button onClick={() => connect('spotify')}>Connect Spotify</button></li>
        <li><button onClick={() => connect('youtube')}>Connect YouTube</button></li>
        <li><button onClick={() => connect('soundcloud')}>Connect SoundCloud</button></li>
      </ul>
    </main>
  )
}
