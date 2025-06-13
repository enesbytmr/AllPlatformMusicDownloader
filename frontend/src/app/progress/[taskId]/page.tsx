'use client'
import { useEffect, useState, useContext } from 'react'
import { AuthContext } from '../../AuthContext'
import { useRouter } from 'next/navigation'

export default function Progress({ params }: { params: { taskId: string } }) {
  const { taskId } = params
  const [status, setStatus] = useState('PENDING')
  const { token } = useContext(AuthContext)
  const router = useRouter()

  useEffect(() => {
    const timer = setInterval(async () => {
      const resp = await fetch(`http://localhost:8000/status/${taskId}`)
      if (resp.ok) {
        const data = await resp.json()
        setStatus(data.status)
        if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
          clearInterval(timer)
        }
      }
    }, 2000)
    return () => clearInterval(timer)
  }, [taskId])

  const download = async () => {
    const resp = await fetch(`http://localhost:8000/download/file/${taskId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (resp.ok) {
      const blob = await resp.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${taskId}.zip`
      a.click()
      window.URL.revokeObjectURL(url)
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Task Progress</h1>
      <p>Status: {status}</p>
      {status === 'SUCCESS' && (
        <button onClick={download}>Download Files</button>
      )}
      {(status === 'SUCCESS' || status === 'FAILURE') && (
        <p><a href={`/downloads/${taskId}`}>View Summary</a></p>
      )}
    </main>
  )
}
