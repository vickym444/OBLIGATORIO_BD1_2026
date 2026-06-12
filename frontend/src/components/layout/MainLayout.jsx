import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopHeader from './TopHeader'

function MainLayout() {
  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main-area">
        <TopHeader />

        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout