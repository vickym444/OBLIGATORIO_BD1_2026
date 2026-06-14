import { Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

export function ProtectedRoute({ children, requiredRole = null }) {
  const { isAuthenticated, isLoading, user } = useAuth()

  if (isLoading) {
    return <div className="loading">Cargando...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && !user?.rol.includes(requiredRole)) {
    return (
      <div className="forbidden-page">
        <h1>Acceso denegado</h1>
        <p>No tienes permisos para acceder a esta página.</p>
        <a href="/">Volver al inicio</a>
      </div>
    )
  }

  return children
}
