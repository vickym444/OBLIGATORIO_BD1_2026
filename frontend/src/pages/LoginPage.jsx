import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { request } from '../services/apiClient'
import '../styles/LoginPage.css'

function LoginPage() {
  const navigate = useNavigate()
  const { login, isAuthenticated, error: authError, setAuthError } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // Si ya está autenticado, redirige a inicio
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setAuthError(null)

    const usernameVal = username.trim()
    const passwordVal = password.trim()

    if (!usernameVal || !passwordVal) {
      setError('Usuario y contraseña son obligatorios')
      return
    }

    setIsLoading(true)

    try {
      const response = await request('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          username: usernameVal,
          password: passwordVal,
        }),
      })

      const { access_token, user } = response.data

      login(access_token, user)
      navigate('/')
    } catch (err) {
      setError(err.message || 'Error al autenticar')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Gestión de Prácticas</h1>
        <p className="login-subtitle">Inicia sesión para continuar</p>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Usuario</label>
            <input
              id="username"
              type="text"
              placeholder="Tu usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="Tu contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />
          </div>

          {error && <p className="error-message">{error}</p>}
          {authError && <p className="error-message">{authError}</p>}

          <button type="submit" disabled={isLoading} className="login-button">
            {isLoading ? 'Autenticando...' : 'Inicia sesión'}
          </button>
        </form>

        <p className="login-footer">
          Usuario de prueba: <strong>admin</strong> / <strong>admin123</strong>
        </p>
      </div>
    </div>
  )
}

export default LoginPage
