import { NavLink } from 'react-router-dom'
import { navigationItems } from './navigation'
import { useAuth } from '../../contexts/AuthContext'

function Sidebar() {
  const { hasRole } = useAuth()
  const isStudent = hasRole('estudiante')

  const items = isStudent
    ? navigationItems.filter((item) => item.path === '/practicas' || item.path === '/inscripciones')
    : navigationItems

  return (
    <aside className="app-sidebar">
      <div className="app-sidebar__brand">
        <p className="app-sidebar__eyebrow">Sistema universitario</p>
        <h1 className="app-sidebar__title">Actividades deportivas</h1>
      </div>

      <nav className="app-sidebar__nav" aria-label="Navegación principal">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              ['app-sidebar__link', isActive ? 'app-sidebar__link--active' : '']
                .filter(Boolean)
                .join(' ')
            }
          >
            <span className="app-sidebar__bullet" aria-hidden="true" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

    </aside>
  )
}

export default Sidebar