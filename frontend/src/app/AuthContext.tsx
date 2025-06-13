'use client'
import { createContext, useState, useEffect, ReactNode } from 'react'

interface AuthContextValue {
  token: string | null
  setToken: (token: string | null) => void
  loaded: boolean
}

export const AuthContext = createContext<AuthContextValue>({
  token: null,
  setToken: () => {},
  loaded: false,
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setTokenState(localStorage.getItem('token'))
    }
    setLoaded(true)
  }, [])

  const setToken = (val: string | null) => {
    setTokenState(val)
    if (typeof window !== 'undefined') {
      if (val) {
        localStorage.setItem('token', val)
      } else {
        localStorage.removeItem('token')
      }
    }
  }

  return (
    <AuthContext.Provider value={{ token, setToken, loaded }}>
      {children}
    </AuthContext.Provider>
  )
}
