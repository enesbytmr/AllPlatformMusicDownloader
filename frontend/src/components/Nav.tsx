"use client"

import { useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '@/app/AuthContext'

export default function Nav() {
  const { token, setToken } = useContext(AuthContext)
  const router = useRouter()
  const logout = () => {
    setToken(null)
    router.push('/')
  }
  return (
    <nav style={{ padding: '1rem', display: 'flex', gap: '1rem', borderBottom: '1px solid #ccc' }}>
      <a href="/">Home</a>
      {token && <a href="/dashboard">Dashboard</a>}
      {token && <a href="/connect">Connect</a>}
      {token && <a href="/plans">Plans</a>}
      {!token && <a href="/login">Login</a>}
      {!token && <a href="/register">Register</a>}
      {token && <button onClick={logout}>Logout</button>}
    </nav>
  )
}
