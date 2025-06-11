'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const resp = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (resp.ok) {
      const data = await resp.json()
      localStorage.setItem('token', data.access_token)
      router.push('/upload')
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
