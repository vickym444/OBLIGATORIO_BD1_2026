import { useEffect, useMemo, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import { listarPracticasParaAsistencia, guardarAsistenciasLote } from '../services/asistenciaService'

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

function buildAsistenciaMap(practicas) {
  const map = {}

  practicas.forEach((practica) => {
    ;(practica.inscriptos ?? []).forEach((inscripcion) => {
      map[inscripcion.id_inscripcion] = Boolean(inscripcion.presente)
    })
  })

  return map
}

function formatPercent(value) {
  const numeric = Number(value ?? 0)
  if (Number.isInteger(numeric)) {
    return String(numeric)
  }
  return numeric.toFixed(2).replace(/\.00$/, '')
}

function AsistenciasPage() {
  const [practicas, setPracticas] = useState([])
  const [asistencias, setAsistencias] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [consultaActiva, setConsultaActiva] = useState('')
  const [fechaDesde, setFechaDesde] = useState(new Date().toISOString().slice(0, 10))
  const [fechaHasta, setFechaHasta] = useState(getTodayPlusDays(7))

  async function cargarPracticas(desde, hasta) {
    const response = await listarPracticasParaAsistencia(desde, hasta)
    const practicasRespuesta = response?.data ?? []

    setPracticas(practicasRespuesta)
    setAsistencias(buildAsistenciaMap(practicasRespuesta))
    setConsultaActiva(`Rango ${desde} a ${hasta}`)
  }

  useEffect(() => {
    let mounted = true

    async function cargarInicialmente() {
      try {
        setIsLoading(true)
        setError('')

        const response = await listarPracticasParaAsistencia(fechaDesde, fechaHasta)
        if (mounted) {
          const practicasRespuesta = response?.data ?? []
          setPracticas(practicasRespuesta)
          setAsistencias(buildAsistenciaMap(practicasRespuesta))
          setConsultaActiva(`Rango ${fechaDesde} a ${fechaHasta}`)
        }
      } catch (requestError) {
        if (mounted) {
          setError(requestError.message || 'No se pudieron cargar las asistencias')
        }
      } finally {
        if (mounted) {
          setIsLoading(false)
        }
      }
    }

    cargarInicialmente()

    return () => {
      mounted = false
    }
  }, [])

  const practicasAgrupadas = useMemo(() => {
    const grupos = new Map()

    practicas.forEach((practica) => {
      if (!grupos.has(practica.fecha)) {
        grupos.set(practica.fecha, [])
      }

      grupos.get(practica.fecha).push(practica)
    })

    return Array.from(grupos.entries()).map(([fecha, practicasGrupo]) => ({
      fecha,
      practicas: practicasGrupo,
    }))
  }, [practicas])

  async function handleConsultar(event) {
    event.preventDefault()

    try {
      setIsLoading(true)
      setError('')
      setSuccessMessage('')
      await cargarPracticas(fechaDesde, fechaHasta)
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron cargar las asistencias')
    } finally {
      setIsLoading(false)
    }
  }

  async function handleGuardar(event) {
    event.preventDefault()

    const registros = practicas.flatMap((practica) =>
      (practica.inscriptos ?? []).map((inscripcion) => ({
        id_inscripcion: inscripcion.id_inscripcion,
        presente: Boolean(asistencias[inscripcion.id_inscripcion]),
      })),
    )

    if (registros.length === 0) {
      setError('No hay inscriptos confirmados para guardar')
      return
    }

    try {
      setIsSaving(true)
      setError('')
      setSuccessMessage('')

      await guardarAsistenciasLote(registros)
      await cargarPracticas(fechaDesde, fechaHasta)
      setSuccessMessage('Asistencias guardadas correctamente')
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron guardar las asistencias')
    } finally {
      setIsSaving(false)
    }
  }

  function handleChangePresente(idInscripcion, checked) {
    setAsistencias((current) => ({
      ...current,
      [idInscripcion]: checked,
    }))
  }

  return (
    <PageShell
      eyebrow="Operación"
      title="Asistencias"
      description="Registra la presencia de los inscriptos confirmados por práctica, filtrando por rango de fechas."
    >
      <CrudCard title="Filtros de prácticas">
        <form className="crud-form" onSubmit={handleConsultar}>
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
          </div>

          <div className="crud-form__actions">
            <button type="submit">Consultar</button>
          </div>
        </form>

        {error ? <p className="crud-message crud-message--error">{error}</p> : null}
        {successMessage ? <p className="crud-message crud-message--success">{successMessage}</p> : null}
      </CrudCard>

      <CrudCard title="Registro de asistencias">
        {isLoading ? <p>Cargando prácticas...</p> : null}

        {!isLoading && practicasAgrupadas.length === 0 ? <p>No hay prácticas en el rango seleccionado.</p> : null}

        {!isLoading && practicasAgrupadas.length > 0 ? (
          <form className="attendance-form" onSubmit={handleGuardar}>
            {consultaActiva ? <p className="attendance-summary">{consultaActiva}</p> : null}

            <div className="attendance-groups">
              {practicasAgrupadas.map(({ fecha, practicas: practicasGrupo }) => (
                <section className="attendance-group" key={fecha}>
                  <header className="attendance-group__header">
                    <h3>{fecha}</h3>
                    <span>{practicasGrupo.length} práctica(s)</span>
                  </header>

                  <div className="attendance-list">
                    {practicasGrupo.map((practica) => (
                      <details className="attendance-practice" key={practica.id_practica}>
                        <summary className="attendance-practice__summary">
                          <div className="attendance-practice__meta">
                            <strong>{practica.actividad_nombre}</strong>
                            <span>{practica.disciplina_nombre}</span>
                            <span>
                              {formatTime(practica.hora_inicio)} a {formatTime(practica.hora_fin)}
                            </span>
                          </div>

                          <div className="attendance-practice__counter">
                            <span>{practica.total_presentes ?? 0} presentes</span>
                            <span>{practica.total_inscriptos ?? 0} confirmados</span>
                            <span>{formatPercent(practica.porcentaje_asistencia)}% asistencia</span>
                          </div>
                        </summary>

                        <div className="attendance-practice__body">
                          {(practica.inscriptos ?? []).length === 0 ? (
                            <p className="attendance-empty">
                              No hay inscriptos confirmados para esta práctica.
                            </p>
                          ) : (
                            <div className="attendance-students">
                              {(practica.inscriptos ?? []).map((inscripcion) => (
                                <label className="attendance-student" key={inscripcion.id_inscripcion}>
                                  <div className="attendance-student__info">
                                    <strong>
                                      {`${inscripcion.estudiante_nombre ?? ''} ${inscripcion.estudiante_apellido ?? ''}`.trim()}
                                    </strong>
                                    <span>CI: {inscripcion.ci}</span>
                                    <span>Facultad: {inscripcion.facultad_nombre}</span>
                                    <span>Carrera: {inscripcion.carrera_nombre}</span>
                                  </div>

                                  <div className="attendance-student__control">
                                    <span>Asistió</span>
                                    <input
                                      type="checkbox"
                                      checked={Boolean(asistencias[inscripcion.id_inscripcion])}
                                      onChange={(event) =>
                                        handleChangePresente(inscripcion.id_inscripcion, event.target.checked)
                                      }
                                    />
                                  </div>
                                </label>
                              ))}
                            </div>
                          )}
                        </div>
                      </details>
                    ))}
                  </div>
                </section>
              ))}
            </div>

            <div className="crud-form__actions attendance-actions">
              <button type="submit" disabled={isSaving}>
                {isSaving ? 'Guardando...' : 'Guardar'}
              </button>
            </div>
          </form>
        ) : null}
      </CrudCard>
    </PageShell>
  )
}

export default AsistenciasPage