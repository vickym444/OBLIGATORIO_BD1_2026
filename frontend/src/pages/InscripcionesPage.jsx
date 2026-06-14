import { useEffect, useMemo, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import { useAuth } from '../contexts/AuthContext'
import { cancelarInscripcion, listarInscripcionesAdmin, listarMisInscripciones } from '../services/inscripcionService'
import { listarFacultades } from '../services/facultadService'
import { listarCarreras } from '../services/carreraService'
import { listarActividades } from '../services/actividadService'
import { listarDisciplinas } from '../services/disciplinaService'

function getTodayPlusDays(days) {
  const now = new Date()
  now.setDate(now.getDate() + days)
  return now.toISOString().slice(0, 10)
}

function formatTime(value) {
  if (typeof value !== 'number') {
    return value ?? ''
  }

  const hours = String(Math.floor(value / 3600)).padStart(2, '0')
  const minutes = String(Math.floor((value % 3600) / 60)).padStart(2, '0')
  return `${hours}:${minutes}`
}

function InscripcionesPage() {
  const { user, hasRole } = useAuth()
  const isAdmin = hasRole('admin')
  const isStudent = hasRole('estudiante')

  const [inscripciones, setInscripciones] = useState([])
  const [facultades, setFacultades] = useState([])
  const [carreras, setCarreras] = useState([])
  const [actividades, setActividades] = useState([])
  const [disciplinas, setDisciplinas] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [cancelandoId, setCancelandoId] = useState(null)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [cantidadVisualizada, setCantidadVisualizada] = useState(0)
  const [fechaDesde, setFechaDesde] = useState(new Date().toISOString().slice(0, 10))
  const [fechaHasta, setFechaHasta] = useState(getTodayPlusDays(7))
  const [filtroFacultad, setFiltroFacultad] = useState('')
  const [filtroCarrera, setFiltroCarrera] = useState('')
  const [filtroActividad, setFiltroActividad] = useState('')
  const [filtroDisciplina, setFiltroDisciplina] = useState('')

  useEffect(() => {
    let mounted = true

    async function cargarDatos() {
      try {
        setIsLoading(true)
        setError('')

        if (isAdmin) {
          const [inscripcionesResponse, facultadesResponse, carrerasResponse, actividadesResponse, disciplinasResponse] =
            await Promise.all([
              listarInscripcionesAdmin({
                fechaDesde,
                fechaHasta,
                idFacultad: filtroFacultad,
                idCarrera: filtroCarrera,
                idActividad: filtroActividad,
                idDisciplina: filtroDisciplina,
              }),
              listarFacultades(),
              listarCarreras(),
              listarActividades(),
              listarDisciplinas(),
            ])

          if (mounted) {
            const inscripcionesData = inscripcionesResponse?.data ?? []
            setInscripciones(inscripcionesData)
            setCantidadVisualizada(inscripcionesResponse?.count ?? inscripcionesData.length)
            setFacultades(facultadesResponse?.data ?? [])
            setCarreras(carrerasResponse?.data ?? [])
            setActividades(actividadesResponse?.data ?? [])
            setDisciplinas(disciplinasResponse?.data ?? [])
          }
        } else if (isStudent) {
          const response = await listarMisInscripciones()
          if (mounted) {
            const inscripcionesData = response?.data ?? []
            setInscripciones(inscripcionesData)
            setCantidadVisualizada(inscripcionesData.length)
          }
        }
      } catch (requestError) {
        if (mounted) {
          setError(requestError.message || 'No se pudieron cargar las inscripciones')
        }
      } finally {
        if (mounted) {
          setIsLoading(false)
        }
      }
    }

    cargarDatos()

    return () => {
      mounted = false
    }
  }, [
    isAdmin,
    isStudent,
    fechaDesde,
    fechaHasta,
    filtroFacultad,
    filtroCarrera,
    filtroActividad,
    filtroDisciplina,
  ])

  const carrerasPorFacultad = useMemo(() => {
    return carreras.filter((carrera) => !filtroFacultad || String(carrera.id_facultad) === filtroFacultad)
  }, [carreras, filtroFacultad])

  async function recargarAdmin(nuevoDesde = fechaDesde, nuevoHasta = fechaHasta) {
    const response = await listarInscripcionesAdmin({
      fechaDesde: nuevoDesde,
      fechaHasta: nuevoHasta,
      idFacultad: filtroFacultad,
      idCarrera: filtroCarrera,
      idActividad: filtroActividad,
      idDisciplina: filtroDisciplina,
    })
    const inscripcionesData = response?.data ?? []
    setInscripciones(inscripcionesData)
    setCantidadVisualizada(response?.count ?? inscripcionesData.length)
  }

  async function handleAplicarRango(event) {
    event.preventDefault()
    try {
      setIsLoading(true)
      setError('')
      await recargarAdmin(fechaDesde, fechaHasta)
    } catch (requestError) {
      setError(requestError.message || 'No se pudo actualizar el rango')
    } finally {
      setIsLoading(false)
    }
  }

  async function handleCancelar(inscripcion) {
    try {
      setCancelandoId(inscripcion.id_inscripcion)
      setError('')
      setSuccessMessage('')

      await cancelarInscripcion(inscripcion.id_inscripcion, new Date().toISOString().slice(0, 10))

      if (isAdmin) {
        await recargarAdmin()
      } else {
        const response = await listarMisInscripciones()
        const inscripcionesData = response?.data ?? []
        setInscripciones(inscripcionesData)
        setCantidadVisualizada(inscripcionesData.length)
      }

      setSuccessMessage('Inscripción dada de baja')
    } catch (requestError) {
      setError(requestError.message || 'No se pudo cancelar la inscripción')
    } finally {
      setCancelandoId(null)
    }
  }

  return (
    <PageShell
      eyebrow="Operación"
      title="Inscripciones"
      description={isAdmin ? 'Revisa todas las inscripciones y aplica filtros por facultad, carrera, actividad, disciplina y fecha.' : 'Consulta y administra tus inscripciones activas en prácticas.'}
    >
      {isAdmin ? (
        <CrudCard title="Panel de inscripciones">
          <form className="crud-form" onSubmit={handleAplicarRango}>
            <div className="crud-form__grid">
              <CrudField
                label="Fecha desde"
                name="fechaDesde"
                value={fechaDesde}
                onChange={(event) => setFechaDesde(event.target.value)}
                type="date"
              />
              <CrudField
                label="Fecha hasta"
                name="fechaHasta"
                value={fechaHasta}
                onChange={(event) => setFechaHasta(event.target.value)}
                type="date"
              />
              <CrudField
                label="Facultad"
                name="filtroFacultad"
                value={filtroFacultad}
                onChange={(event) => {
                  setFiltroFacultad(event.target.value)
                  setFiltroCarrera('')
                }}
                as="select"
                options={[{ value: '', label: 'Todas' }, ...facultades.map((facultad) => ({ value: facultad.id_facultad, label: facultad.nombre }))]}
              />
              <CrudField
                label="Carrera"
                name="filtroCarrera"
                value={filtroCarrera}
                onChange={(event) => setFiltroCarrera(event.target.value)}
                as="select"
                options={[{ value: '', label: 'Todas' }, ...carrerasPorFacultad.map((carrera) => ({ value: carrera.id_carrera, label: carrera.nombre }))]}
              />
              <CrudField
                label="Actividad"
                name="filtroActividad"
                value={filtroActividad}
                onChange={(event) => setFiltroActividad(event.target.value)}
                as="select"
                options={[{ value: '', label: 'Todas' }, ...actividades.map((actividad) => ({ value: actividad.id_actividad, label: actividad.nombre }))]}
              />
              <CrudField
                label="Disciplina"
                name="filtroDisciplina"
                value={filtroDisciplina}
                onChange={(event) => setFiltroDisciplina(event.target.value)}
                as="select"
                options={[{ value: '', label: 'Todas' }, ...disciplinas.map((disciplina) => ({ value: disciplina.id_disciplina, label: disciplina.nombre }))]}
              />
            </div>

            <div className="crud-form__actions">
              <button type="submit">Aplicar rango</button>
            </div>
          </form>

          {error ? <p className="crud-message crud-message--error">{error}</p> : null}
          {successMessage ? <p className="crud-message crud-message--success">{successMessage}</p> : null}
        </CrudCard>
      ) : null}

      <CrudCard title={isAdmin ? 'Tabla de inscripciones' : 'Mis inscripciones'}>
        {!isLoading ? <p>Inscripciones visualizadas: {cantidadVisualizada}</p> : null}
        {isLoading ? <p>Cargando inscripciones...</p> : null}
        {!isLoading && inscripciones.length === 0 ? <p>No hay inscripciones para mostrar.</p> : null}

        {!isLoading && inscripciones.length > 0 ? (
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>CI</th>
                  <th>Facultad</th>
                  <th>Carrera</th>
                  <th>Fecha</th>
                  <th>Hora</th>
                  <th>Actividad</th>
                  <th>Disciplina</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {inscripciones.map((inscripcion) => (
                  <tr key={inscripcion.id_inscripcion}>
                    <td>{`${inscripcion.estudiante_nombre ?? ''} ${inscripcion.estudiante_apellido ?? ''}`.trim()}</td>
                    <td>{inscripcion.ci}</td>
                    <td>{inscripcion.facultad_nombre}</td>
                    <td>{inscripcion.carrera_nombre}</td>
                    <td>{inscripcion.fecha_practica}</td>
                    <td>{`${formatTime(inscripcion.hora_inicio)} a ${formatTime(inscripcion.hora_fin)}`}</td>
                    <td>{inscripcion.actividad_nombre}</td>
                    <td>{inscripcion.disciplina_nombre}</td>
                    <td>{inscripcion.estado}</td>
                    <td>
                      <button
                        type="button"
                        className="inscripcion-list__button"
                        onClick={() => handleCancelar(inscripcion)}
                        disabled={cancelandoId === inscripcion.id_inscripcion}
                      >
                        {cancelandoId === inscripcion.id_inscripcion ? 'Dando de baja...' : 'Dar de baja'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </CrudCard>
    </PageShell>
  )
}

export default InscripcionesPage