import { createContext, useContext, useEffect, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  // Restore session from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('auth_user')

    if (storedToken && storedUser) {
      try {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))
      } catch (err) {
        console.error('Failed to restore session', err)
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_user')
      }
    }

    setIsLoading(false)
  }, [])

  function login(tokenValue, userData) {
    setToken(tokenValue)
    setUser(userData)
    setError(null)

    localStorage.setItem('auth_token', tokenValue)
    localStorage.setItem('auth_user', JSON.stringify(userData))
  }

  function logout() {
    setToken(null)
    setUser(null)
    setError(null)

    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }

  function setAuthError(message) {
    setError(message)
  }

  const value = {
    user,
    token,
    isLoading,
    error,
    isAuthenticated: !!token,
    login,
    logout,
    setAuthError,
    hasRole: (role) => user?.rol === role,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
