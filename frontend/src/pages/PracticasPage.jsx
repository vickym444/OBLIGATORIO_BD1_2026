import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import PracticaGroup from '../components/practicas/PracticaGroup'
import { listarActividades } from '../services/actividadService'
import {
  generarPracticas,
  listarPracticasPorFecha,
  listarPracticasPorRango,
} from '../services/practicaService'
import { inscribirseAPractica, listarMisInscripciones } from '../services/inscripcionService'

const today = new Date()
const initialDate = today.toISOString().slice(0, 10)
const initialDateTo = initialDate

function PracticasPage() {
  const { user, hasRole, isAuthenticated, isLoading: isAuthLoading } = useAuth()
  const isAdmin = hasRole('admin')
  const [actividades, setActividades] = useState([])
  const [practicas, setPracticas] = useState([])
  const [misInscripciones, setMisInscripciones] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSearching, setIsSearching] = useState(false)
  const [isLoadingInscripciones, setIsLoadingInscripciones] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [inscribiendoId, setInscribiendoId] = useState(null)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [fechaDesde, setFechaDesde] = useState(initialDate)
  const [fechaHasta, setFechaHasta] = useState(initialDateTo)
  const [actividadId, setActividadId] = useState('')
  const [consultaActiva, setConsultaActiva] = useState('')
  const [ordenarPorcentaje, setOrdenarPorcentaje] = useState(false)
  const [soloCuposDisponibles, setSoloCuposDisponibles] = useState(false)

  useEffect(() => {
    if (isAuthLoading) {
      return undefined
    }

    let isMounted = true

    async function cargarDatosIniciales() {
      try {
        setIsLoading(true)
        setError('')

        const [actividadesResponse, inscripcionesResponse] = await Promise.all([
          listarActividades(),
          isAuthenticated && hasRole('estudiante') ? listarMisInscripciones() : Promise.resolve({ data: [] }),
        ])

        if (isMounted) {
          setActividades(actividadesResponse?.data ?? [])
          setMisInscripciones(inscripcionesResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las prácticas')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
          setIsLoadingInscripciones(false)
        }
      }
    }

    cargarDatosIniciales()

    return () => {
      isMounted = false
    }
  }, [isAuthLoading, isAuthenticated, hasRole])

  function getLocalDateString() {
    const now = new Date()
    const offsetMinutes = now.getTimezoneOffset()
    const localDate = new Date(now.getTime() - offsetMinutes * 60 * 1000)
    return localDate.toISOString().slice(0, 10)
  }

  const misInscripcionesPorPractica = useMemo(() => {
    return new Map(misInscripciones.map((inscripcion) => [inscripcion.id_practica, inscripcion]))
  }, [misInscripciones])

  const practicasAgrupadas = useMemo(() => {
    const grupos = new Map()

    practicas.forEach((practica) => {
      if (!grupos.has(practica.fecha)) {
        grupos.set(practica.fecha, [])
      }

      grupos.get(practica.fecha).push(practica)
    })

    return Array.from(grupos.entries()).map(([fechaGrupo, practicasGrupo]) => ({
      fecha: fechaGrupo,
      practicas: practicasGrupo,
    }))
  }, [practicas])

  async function cargarPracticasActuales({ preservarConsulta = true } = {}) {
    if (!fechaDesde || !fechaHasta) {
      setError('Debes seleccionar fecha desde y fecha hasta')
      return
    }

    const response = await listarPracticasPorRango(fechaDesde, fechaHasta, ordenarPorcentaje, soloCuposDisponibles)
    setPracticas(response?.data ?? [])
    if (preservarConsulta) {
      setConsultaActiva(`Rango ${fechaDesde} a ${fechaHasta}`)
    }
  }

  async function consultarPracticas(event) {
    event.preventDefault()

    try {
      setIsSearching(true)
      setError('')

      await cargarPracticasActuales()
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron consultar las prácticas')
    } finally {
      setIsSearching(false)
    }
  }

  async function handleOrdenarPorcentajeChange(event) {
    const checked = event.target.checked
    setOrdenarPorcentaje(checked)

    if (!consultaActiva) {
      return
    }

    try {
      setIsSearching(true)
      setError('')
      await (async () => {
        const response = await listarPracticasPorRango(fechaDesde, fechaHasta, checked, soloCuposDisponibles)
        setPracticas(response?.data ?? [])
      })()
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron reordenar las prácticas')
    } finally {
      setIsSearching(false)
    }
  }

  async function handleSoloCuposDisponiblesChange(event) {
    const checked = event.target.checked
    setSoloCuposDisponibles(checked)

    if (!consultaActiva) {
      return
    }

    try {
      setIsSearching(true)
      setError('')
      await (async () => {
        const response = await listarPracticasPorRango(fechaDesde, fechaHasta, ordenarPorcentaje, checked)
        setPracticas(response?.data ?? [])
      })()
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron filtrar las prácticas')
    } finally {
      setIsSearching(false)
    }
  }

  async function handleGenerarPracticas() {
    const idActividad = Number(actividadId)

    if (!idActividad) {
      setError('Debes seleccionar una actividad para generar prácticas')
      return
    }

    try {
      setIsGenerating(true)
      setError('')

      await generarPracticas(idActividad, fechaDesde || undefined, fechaHasta || undefined)

      if (consultaActiva) {
        const response = await listarPracticasPorRango(
          fechaDesde,
          fechaHasta,
          ordenarPorcentaje,
          soloCuposDisponibles,
        )

        setPracticas(response?.data ?? [])
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron generar las prácticas')
    } finally {
      setIsGenerating(false)
    }
  }

  function getActividadNombre(idActividad) {
    const actividad = actividades.find((item) => item.id_actividad === idActividad)
    return actividad?.nombre ?? `Actividad ${idActividad}`
  }

  function getDetalleActividad(idActividad) {
    const actividad = actividades.find((item) => item.id_actividad === idActividad)
    if (!actividad) {
      return ''
    }

    return `${actividad.dia} · ${actividad.hora_inicio} a ${actividad.hora_fin}`
  }

  function getEstadoInscripcion(idPractica) {
    return misInscripcionesPorPractica.get(idPractica) ?? null
  }

  async function handleInscribir(practica) {
    if (!user?.id_estudiante) {
      setError('Solo los estudiantes pueden inscribirse')
      return
    }

    try {
      setInscribiendoId(practica.id_practica)
      setError('')
      setSuccessMessage('')

      const response = await inscribirseAPractica(practica.id_practica, user.id_estudiante, getLocalDateString())
      const estadoNuevo = response?.data?.id_inscripcion ? 'Inscripción realizada' : 'Inscripción procesada'

      const inscripcionesResponse = await listarMisInscripciones()
      setMisInscripciones(inscripcionesResponse?.data ?? [])
      setSuccessMessage(estadoNuevo)
    } catch (requestError) {
      setError(requestError.message || 'No se pudo completar la inscripción')
    } finally {
      setInscribiendoId(null)
    }
  }

  const puedeInscribirse = isAuthenticated && hasRole('estudiante') && !isLoadingInscripciones

  return (
    <PageShell
      eyebrow="Operación"
      title="Prácticas"
      description="Consulta las instancias concretas de las actividades por fecha o rango, con posibilidad de regenerar prácticas futuras."
    >
      <section className="panel practice-grid">
        <CrudCard title="Filtros y generación">
          <form className="crud-form" onSubmit={consultarPracticas}>
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
                label="Actividad para generar"
                name="actividadId"
                value={actividadId}
                onChange={(event) => setActividadId(event.target.value)}
                as="select"
                placeholder="Seleccionar actividad"
                options={actividades.map((actividad) => ({
                  value: actividad.id_actividad,
                  label: actividad.nombre,
                }))}
                className="crud-field--full"
              />

              {isAdmin ? (
                <>
                  <label className="practice-sort-toggle crud-field--full">
                    <input
                      type="checkbox"
                      checked={ordenarPorcentaje}
                      onChange={handleOrdenarPorcentajeChange}
                    />
                    <span>Ordenar por porcentaje de inscriptos</span>
                  </label>

                  <label className="practice-sort-toggle crud-field--full">
                    <input
                      type="checkbox"
                      checked={soloCuposDisponibles}
                      onChange={handleSoloCuposDisponiblesChange}
                    />
                    <span>Mostrar solo prácticas con cupos disponibles</span>
                  </label>
                </>
              ) : null}
            </div>

            <div className="crud-form__actions">
              <button type="submit" disabled={isSearching || isLoading}>
                {isSearching ? 'Consultando...' : 'Consultar prácticas'}
              </button>

              <button type="button" onClick={handleGenerarPracticas} disabled={isGenerating || isLoading}>
                {isGenerating ? 'Generando...' : 'Generar prácticas'}
              </button>
            </div>
          </form>

          {error ? <p className="crud-message crud-message--error">{error}</p> : null}
          {successMessage ? <p className="crud-message crud-message--success">{successMessage}</p> : null}
          <p className="practice-helper">
            La consulta muestra solo prácticas activas. La generación usa la actividad seleccionada como base.
          </p>
        </CrudCard>

        <CrudCard title={consultaActiva ? `Resultado: ${consultaActiva}` : 'Listado de prácticas'}>
          {isLoading ? <p>Cargando actividades...</p> : null}

          {!isLoading && !error && practicas.length === 0 ? (
            <p>No hay prácticas para el criterio seleccionado.</p>
          ) : null}

          {!isLoading && practicasAgrupadas.length > 0 ? (
            <div className="practice-groups">
              {practicasAgrupadas.map((grupo) => (
                <PracticaGroup
                  key={grupo.fecha}
                  fecha={grupo.fecha}
                  practicas={grupo.practicas}
                  getActividadNombre={getActividadNombre}
                  getDetalleActividad={getDetalleActividad}
                  getEstadoInscripcion={getEstadoInscripcion}
                  onInscribir={puedeInscribirse ? handleInscribir : null}
                  isInscribiendoId={inscribiendoId}
                  canInscribir={puedeInscribirse}
                />
              ))}
            </div>
          ) : null}
        </CrudCard>
      </section>
    </PageShell>
  )
}

export default PracticasPage