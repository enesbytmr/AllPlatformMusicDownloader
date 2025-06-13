'use client'
import { useContext, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '../../AuthContext'

interface Info {
  status: string
  failed?: string[]
}

export default function DownloadSummary({ params }: { params: { taskId: string } }) {
  const { token, loaded } = useContext(AuthContext)
  const router = useRouter()
  const { taskId } = params
  const [info, setInfo] = useState<Info>({ status: 'PENDING' })

  useEffect(() => {
    if (loaded && !token) {
      router.push('/login')
      return
    }
    fetch(`http://localhost:8000/status/${taskId}`)
      .then(r => r.ok && r.json())
      .then(data => data && setInfo(data))
  }, [loaded, token, taskId])

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

  const retry = async () => {
    if (!info.failed || !info.failed.length) return
    const form = new FormData()
    const file = new Blob([info.failed.join('\n')], { type: 'text/plain' })
    form.append('file', file, 'tracks.txt')
    const resp = await fetch('http://localhost:8000/download/text', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: form
    })
    if (resp.ok) {
      const data = await resp.json()
      router.push(`/progress/${data.task_id}`)
    } else {
      alert('Retry failed')
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Download Summary</h1>
      <p>Status: {info.status}</p>
      {info.failed && info.failed.length > 0 && (
        <>
          <h2>Failed Tracks</h2>
          <ul>{info.failed.map((t, i) => <li key={i}>{t}</li>)}</ul>
          <button onClick={retry}>Retry Failed</button>
        </>
      )}
      {info.status === 'SUCCESS' && <button onClick={download}>Download Files</button>}
    </main>
  )
}
