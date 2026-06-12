import { useLocation } from 'react-router-dom'
import { sectionLabels } from './navigation'

function TopHeader() {
  const location = useLocation()
  const currentSection = sectionLabels[location.pathname] ?? 'Dashboard'

  return (
    <header className="app-header">
      <div className="app-header__meta">
        <p className="app-header__eyebrow">Panel principal</p>
        <h2 className="app-header__title">{currentSection}</h2>
        <p className="app-header__subtitle">
          Navegación base preparada para los módulos del sistema.
        </p>
      </div>

      <div className="app-header__badge">React + Router + Vite</div>
    </header>
  )
}

export default TopHeader