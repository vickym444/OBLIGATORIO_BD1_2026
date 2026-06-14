import { useEffect, useMemo, useState } from 'react'
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

const today = new Date()
const initialDate = today.toISOString().slice(0, 10)
const oneWeekAhead = new Date(today)
oneWeekAhead.setDate(oneWeekAhead.getDate() + 7)
const initialDateTo = oneWeekAhead.toISOString().slice(0, 10)

const modeOptions = [
  { value: 'fecha', label: 'Por fecha' },
  { value: 'rango', label: 'Por rango' },
]

function PracticasPage() {
  const [actividades, setActividades] = useState([])
  const [practicas, setPracticas] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSearching, setIsSearching] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState('fecha')
  const [fecha, setFecha] = useState(initialDate)
  const [fechaDesde, setFechaDesde] = useState(initialDate)
  const [fechaHasta, setFechaHasta] = useState(initialDateTo)
  const [actividadId, setActividadId] = useState('')
  const [consultaActiva, setConsultaActiva] = useState('')

  useEffect(() => {
    let isMounted = true

    async function cargarDatosIniciales() {
      try {
        setIsLoading(true)
        setError('')

        const actividadesResponse = await listarActividades()

        if (isMounted) {
          setActividades(actividadesResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las prácticas')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarDatosIniciales()

    return () => {
      isMounted = false
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

    return Array.from(grupos.entries()).map(([fechaGrupo, practicasGrupo]) => ({
      fecha: fechaGrupo,
      practicas: practicasGrupo,
    }))
  }, [practicas])

  function handleModeChange(event) {
    setMode(event.target.value)
    setError('')
  }

  async function consultarPracticas(event) {
    event.preventDefault()

    try {
      setIsSearching(true)
      setError('')

      if (mode === 'rango') {
        if (!fechaDesde || !fechaHasta) {
          setError('Debes seleccionar fecha desde y fecha hasta')
          return
        }

        const response = await listarPracticasPorRango(fechaDesde, fechaHasta)
        setPracticas(response?.data ?? [])
        setConsultaActiva(`Rango ${fechaDesde} a ${fechaHasta}`)
        return
      }

      if (!fecha) {
        setError('Debes seleccionar una fecha')
        return
      }

      const response = await listarPracticasPorFecha(fecha)
      setPracticas(response?.data ?? [])
      setConsultaActiva(`Fecha ${fecha}`)
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron consultar las prácticas')
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
        const response =
          mode === 'rango'
            ? await listarPracticasPorRango(fechaDesde, fechaHasta)
            : await listarPracticasPorFecha(fecha)

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
                label="Modo de consulta"
                name="mode"
                value={mode}
                onChange={handleModeChange}
                as="select"
                options={modeOptions}
                className="crud-field--full"
              />

              {mode === 'fecha' ? (
                <CrudField
                  label="Fecha"
                  name="fecha"
                  value={fecha}
                  onChange={(event) => setFecha(event.target.value)}
                  type="date"
                  className="crud-field--full"
                />
              ) : null}

              {mode === 'rango' ? (
                <>
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
                </>
              ) : null}

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