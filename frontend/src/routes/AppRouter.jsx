import { Navigate, Route, Routes } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import DashboardPage from '../pages/DashboardPage'
import FacultadesPage from '../pages/FacultadesPage'
import CarrerasPage from '../pages/CarrerasPage'
import EstudiantesPage from '../pages/EstudiantesPage'
import DisciplinasPage from '../pages/DisciplinasPage'
import EspaciosPage from '../pages/EspaciosPage'
import ActividadesPage from '../pages/ActividadesPage'
import InscripcionesPage from '../pages/InscripcionesPage'
import AsistenciasPage from '../pages/AsistenciasPage'
import ReportesPage from '../pages/ReportesPage'
import UsuariosPage from '../pages/UsuariosPage'

function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="facultades" element={<FacultadesPage />} />
        <Route path="carreras" element={<CarrerasPage />} />
        <Route path="estudiantes" element={<EstudiantesPage />} />
        <Route path="disciplinas" element={<DisciplinasPage />} />
        <Route path="espacios" element={<EspaciosPage />} />
        <Route path="actividades" element={<ActividadesPage />} />
        <Route path="inscripciones" element={<InscripcionesPage />} />
        <Route path="asistencias" element={<AsistenciasPage />} />
        <Route path="reportes" element={<ReportesPage />} />
        <Route path="usuarios" element={<UsuariosPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default AppRouter