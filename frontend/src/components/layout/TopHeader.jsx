import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { sectionLabels } from './navigation'

function TopHeader() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const currentSection = sectionLabels[location.pathname] ?? 'Dashboard'

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <header className="app-header">
      <div className="app-header__meta">
        <p className="app-header__eyebrow">Panel principal</p>
        <h2 className="app-header__title">{currentSection}</h2>
        <p className="app-header__subtitle">
          Navegación base preparada para los módulos del sistema.
        </p>
      </div>

      <div className="app-header__controls">
        <div className="app-header__user">
          <span className="app-header__username">{user?.username}</span>
          <span className={`app-header__role app-header__role--${user?.rol}`}>
            {user?.rol === 'admin' ? 'Administrador' : 'Estudiante'}
          </span>
        </div>
        <button onClick={handleLogout} className="app-header__logout">
          Cerrar sesión
        </button>
      </div>
    </header>
  )
}

export default TopHeader