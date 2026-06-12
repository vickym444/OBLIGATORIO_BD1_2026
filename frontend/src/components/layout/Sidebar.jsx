import { NavLink } from 'react-router-dom'
import { navigationItems } from './navigation'

function Sidebar() {
  return (
    <aside className="app-sidebar">
      <div className="app-sidebar__brand">
        <p className="app-sidebar__eyebrow">Sistema universitario</p>
        <h1 className="app-sidebar__title">Actividades deportivas</h1>
        <p className="app-sidebar__subtitle">Base de navegación y módulos</p>
      </div>

      <nav className="app-sidebar__nav" aria-label="Navegación principal">
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/dashboard'}
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

      <div className="app-sidebar__footer">
        Estructura base lista para conectar los datos reales del backend.
      </div>
    </aside>
  )
}

export default Sidebar