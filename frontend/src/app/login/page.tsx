'use client'
import { useState, useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../AuthContext'
import { API } from '@/api'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()
  const { setToken } = useContext(AuthContext)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const resp = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (resp.ok) {
      const data = await resp.json()
      setToken(data.access_token)
      router.push('/dashboard')
    } else {
      alert('Login failed')
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Login</h1>
      <form onSubmit={onSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxWidth: '300px' }}>
        <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" type="email" required />
        <input value={password} onChange={e => setPassword(e.target.value)} placeholder="password" type="password" required />
        <button type="submit">Login</button>
      </form>
    </main>
  )
}
