'use client'
import { useState, useEffect, useContext } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../AuthContext'

interface Plan {
  limit: number
  period: string
}

export default function Plans() {
  const { token, loaded } = useContext(AuthContext)
  const router = useRouter()
  const [plans, setPlans] = useState<Record<string, Plan>>({})

  useEffect(() => {
    if (loaded && !token) {
      router.push('/login')
      return
    }
    fetch('http://localhost:8000/billing/plans')
      .then(r => r.json())
      .then(setPlans)
  }, [loaded, token])

  const upgrade = async (plan: string) => {
    const resp = await fetch(`http://localhost:8000/billing/upgrade?plan=${plan}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (resp.ok) {
      const data = await resp.json()
      window.open(data.checkout_url, '_blank')
    } else {
      alert('Upgrade failed')
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Subscription Plans</h1>
      <ul>
        {Object.entries(plans).map(([name, info]) => (
          <li key={name} style={{ marginBottom: '0.5rem' }}>
            <strong>{name}</strong> – {info.limit}/{info.period}
            {token && <button onClick={() => upgrade(name)} style={{ marginLeft: '1rem' }}>Select</button>}
          </li>
        ))}
      </ul>
    </main>
  )
}
