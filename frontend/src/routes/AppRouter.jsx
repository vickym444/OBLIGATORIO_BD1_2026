import { Navigate, Route, Routes } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import LoginPage from '../pages/LoginPage'
import { ProtectedRoute } from '../components/routes/ProtectedRoute'
import FacultadesPage from '../pages/FacultadesPage'
import CarrerasPage from '../pages/CarrerasPage'
import EstudiantesPage from '../pages/EstudiantesPage'
import DisciplinasPage from '../pages/DisciplinasPage'
import EspaciosPage from '../pages/EspaciosPage'
import ActividadesPage from '../pages/ActividadesPage'
import PracticasPage from '../pages/PracticasPage'
import InscripcionesPage from '../pages/InscripcionesPage'
import AsistenciasPage from '../pages/AsistenciasPage'
import ReportesPage from '../pages/ReportesPage'
import UsuariosPage from '../pages/UsuariosPage'

function AppRouter() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected routes */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<PracticasPage />} />
        <Route path="facultades" element={<FacultadesPage />} />
        <Route path="carreras" element={<CarrerasPage />} />
        <Route path="estudiantes" element={<EstudiantesPage />} />
        <Route path="disciplinas" element={<DisciplinasPage />} />
        <Route path="espacios" element={<EspaciosPage />} />
        <Route path="actividades" element={<ActividadesPage />} />
        <Route path="practicas" element={<PracticasPage />} />
        <Route path="inscripciones" element={<InscripcionesPage />} />
        <Route path="asistencias" element={<AsistenciasPage />} />
        <Route path="reportes" element={<ReportesPage />} />
        <Route path="usuarios" element={<UsuariosPage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default AppRouter