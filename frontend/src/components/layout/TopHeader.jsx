import { useAuth } from '../../contexts/AuthContext'
import logoUcu from '../../assets/Logo-Universidad-Catolica.svg'

function TopHeader() {
  const { user, logout } = useAuth()

  function handleLogout() {
    logout()
  }

  return (
    <header className="app-header">
      <div className="app-header__meta">
        <img
          src={logoUcu}
          alt="Logo UCU"
          className="app-header__logo"
        />
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