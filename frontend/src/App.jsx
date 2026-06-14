import { useEffect } from 'react'
import AppRouter from './routes/AppRouter'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { setAuthToken, clearAuthToken } from './services/apiClient'
import './App.css'

function AppWithAuth() {
  const { token } = useAuth()

  useEffect(() => {
    if (token) {
      setAuthToken(token)
    } else {
      clearAuthToken()
    }
  }, [token])

  return <AppRouter />
}

function App() {
  return (
    <AuthProvider>
      <AppWithAuth />
    </AuthProvider>
  )
}

export default App
