import { useEffect, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import { listarDisciplinas } from '../services/disciplinaService'
import { listarEspacios } from '../services/espacioService'
import {
  actualizarActividad,
  crearActividad,
  eliminarActividad,
  listarActividades,
} from '../services/actividadService'

const initialForm = {
  nombre: '',
  cupo_maximo: '',
  cupo_minimo: '',
  hora_inicio: '',
  hora_fin: '',
  dia: '',
  estado: '',
  id_disciplina: '',
  id_espacio: '',
}

const diaOptions = [
  'Lunes',
  'Martes',
  'Miercoles',
  'Jueves',
  'Viernes',
  'Lunes y Miercoles',
  'Martes y Jueves',
  'Miercoles y Viernes',
].map((value) => ({ value, label: value }))

const estadoOptions = ['abierta', 'cerrada', 'finalizada', 'cancelada'].map((value) => ({
  value,
  label: value,
}))

function formatActividadErrorMessage(message) {
  if (message && /superpone|superposición|horario/i.test(message)) {
    return 'El horario y lugar se superpone con otra actividad'
  }

  return message || 'No se pudo guardar la actividad'
}

function formatHora24(hora) {
  if (hora === null || hora === undefined || hora === '') {
    return '--:--'
  }

  if (typeof hora === 'number') {
    const totalSeconds = Math.max(0, Math.floor(hora))
    const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0')
    const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0')
    return `${hours}:${minutes}`
  }

  const text = String(hora)
  const match = text.match(/^(\d{1,2}):(\d{2})/)
  if (!match) {
    return text
  }

  const hours = match[1].padStart(2, '0')
  const minutes = match[2]
  return `${hours}:${minutes}`
}

function ActividadesPage() {
  const [actividades, setActividades] = useState([])
  const [disciplinas, setDisciplinas] = useState([])
  const [espacios, setEspacios] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [formValues, setFormValues] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)

  useEffect(() => {
    let isMounted = true

    async function cargarDatos() {
      try {
        setIsLoading(true)
        setError('')

        const [actividadesResponse, disciplinasResponse, espaciosResponse] = await Promise.all([
          listarActividades(),
          listarDisciplinas(),
          listarEspacios(),
        ])

        if (isMounted) {
          setActividades(actividadesResponse?.data ?? [])
          setDisciplinas(disciplinasResponse?.data ?? [])
          setEspacios(espaciosResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las actividades')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarDatos()

    return () => {
      isMounted = false
    }
  }, [])

  function handleChange(event) {
    const { name, value } = event.target
    setFormValues((currentValues) => ({
      ...currentValues,
      [name]: value,
    }))
  }

  function resetForm() {
    setFormValues(initialForm)
    setEditingId(null)
    setError('')
  }

  async function reloadActividades() {
    const response = await listarActividades()
    setActividades(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nombre = formValues.nombre.trim()
    const cupoMaximo = Number(formValues.cupo_maximo)
    const cupoMinimo = Number(formValues.cupo_minimo)
    const idDisciplina = Number(formValues.id_disciplina)
    const idEspacio = Number(formValues.id_espacio)

    if (!nombre) {
      setError('El nombre de la actividad es obligatorio')
      return
    }

    if (!Number.isInteger(cupoMaximo) || cupoMaximo <= 0) {
      setError('El cupo máximo debe ser un número mayor que 0')
      return
    }

    if (!Number.isInteger(cupoMinimo) || cupoMinimo <= 0) {
      setError('El cupo mínimo debe ser un número mayor que 0')
      return
    }

    if (cupoMinimo > cupoMaximo) {
      setError('El cupo mínimo no puede ser mayor al cupo máximo')
      return
    }

    if (!formValues.hora_inicio || !formValues.hora_fin) {
      setError('Debes completar la hora de inicio y la hora de fin')
      return
    }

    if (!formValues.dia) {
      setError('Debes seleccionar un día')
      return
    }

    if (!formValues.estado) {
      setError('Debes seleccionar un estado')
      return
    }

    if (!idDisciplina) {
      setError('Debes seleccionar una disciplina')
      return
    }

    if (!idEspacio) {
      setError('Debes seleccionar un espacio')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      const payload = {
        nombre,
        cupo_maximo: cupoMaximo,
        cupo_minimo: cupoMinimo,
        hora_inicio: formValues.hora_inicio,
        hora_fin: formValues.hora_fin,
        dia: formValues.dia,
        estado: formValues.estado,
        id_disciplina: idDisciplina,
        id_espacio: idEspacio,
      }

      if (editingId) {
        const current = actividades.find((item) => item.id_actividad === editingId)
        await actualizarActividad(editingId, {
          ...payload,
          activo: current?.activo ?? 1,
        })
      } else {
        await crearActividad(payload)
      }

      await reloadActividades()
      resetForm()
    } catch (requestError) {
      setError(formatActividadErrorMessage(requestError.message))
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(actividad) {
    setEditingId(actividad.id_actividad)
    setFormValues({
      nombre: actividad.nombre,
      cupo_maximo: String(actividad.cupo_maximo),
      cupo_minimo: String(actividad.cupo_minimo),
      hora_inicio: actividad.hora_inicio,
      hora_fin: actividad.hora_fin,
      dia: actividad.dia,
      estado: actividad.estado,
      id_disciplina: String(actividad.id_disciplina),
      id_espacio: String(actividad.id_espacio),
    })
    setError('')
  }

  async function handleDelete(idActividad) {
    const shouldDelete = window.confirm('¿Eliminar esta actividad? Se marcará como inactiva.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarActividad(idActividad)
      await reloadActividades()

      if (editingId === idActividad) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar la actividad')
    }
  }

  function getDisciplinaNombre(idDisciplina) {
    const disciplina = disciplinas.find((item) => item.id_disciplina === idDisciplina)
    return disciplina?.nombre ?? `Disciplina ${idDisciplina}`
  }

  function getEspacioNombre(idEspacio) {
    const espacio = espacios.find((item) => item.id_espacio === idEspacio)
    return espacio?.nombre ?? `Espacio ${idEspacio}`
  }

  return (
    <PageShell
      eyebrow="Operación"
      title="Actividades"
      description="ABM de actividades conectado al backend real, con reactivación de registros inactivos por nombre."
    >
      <section className="panel crud-grid">
        <CrudCard title={editingId ? 'Editar actividad' : 'Nueva actividad'}>
          <form className="crud-form" onSubmit={handleSubmit}>
            <div className="crud-form__grid">
              <CrudField
                label="Nombre"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Futbol matutino"
                className="crud-field--full"
              />

              <CrudField
                label="Cupo máximo"
                name="cupo_maximo"
                value={formValues.cupo_maximo}
                onChange={handleChange}
                type="number"
                min="1"
                placeholder="Ej.: 20"
              />

              <CrudField
                label="Cupo mínimo"
                name="cupo_minimo"
                value={formValues.cupo_minimo}
                onChange={handleChange}
                type="number"
                min="1"
                placeholder="Ej.: 10"
              />

              <CrudField
                label="Hora inicio"
                name="hora_inicio"
                value={formValues.hora_inicio}
                onChange={handleChange}
                type="time"
              />

              <CrudField
                label="Hora fin"
                name="hora_fin"
                value={formValues.hora_fin}
                onChange={handleChange}
                type="time"
              />

              <CrudField
                label="Día"
                name="dia"
                value={formValues.dia}
                onChange={handleChange}
                as="select"
                placeholder="Seleccionar día"
                options={diaOptions}
              />

              <CrudField
                label="Estado"
                name="estado"
                value={formValues.estado}
                onChange={handleChange}
                as="select"
                placeholder="Seleccionar estado"
                options={estadoOptions}
              />

              <CrudField
                label="Disciplina"
                name="id_disciplina"
                value={formValues.id_disciplina}
                onChange={handleChange}
                as="select"
                placeholder="Seleccionar disciplina"
                options={disciplinas.map((disciplina) => ({
                  value: disciplina.id_disciplina,
                  label: disciplina.nombre,
                }))}
              />

              <CrudField
                label="Espacio"
                name="id_espacio"
                value={formValues.id_espacio}
                onChange={handleChange}
                as="select"
                placeholder="Seleccionar espacio"
                options={espacios.map((espacio) => ({
                  value: espacio.id_espacio,
                  label: espacio.nombre,
                }))}
              />
            </div>

            <div className="crud-form__actions">
              <button type="submit" disabled={isSaving}>
                {isSaving ? 'Guardando...' : editingId ? 'Actualizar' : 'Crear'}
              </button>

              {editingId ? (
                <button type="button" onClick={resetForm}>
                  Cancelar
                </button>
              ) : null}
            </div>
          </form>

          {error ? <p className="crud-message crud-message--error">{error}</p> : null}
        </CrudCard>

        <CrudCard title="Listado de actividades">
          {isLoading ? <p>Cargando actividades...</p> : null}

          {!isLoading && !error && actividades.length === 0 ? <p>No hay actividades cargadas.</p> : null}

          {!isLoading && actividades.length > 0 ? (
            <ul className="crud-list">
              {actividades.map((actividad) => (
                <li key={actividad.id_actividad} className="crud-list__item">
                  <div>
                    <strong>{actividad.nombre}</strong>
                    <span>ID {actividad.id_actividad}</span>
                    <span>{actividad.dia}</span>
                    <span>{actividad.estado}</span>
                    <span>
                      Cupos {actividad.cupo_minimo} - {actividad.cupo_maximo}
                    </span>
                    <span>
                      {formatHora24(actividad.hora_inicio)} - {formatHora24(actividad.hora_fin)}
                    </span>
                    <span>{getDisciplinaNombre(actividad.id_disciplina)}</span>
                    <span>{getEspacioNombre(actividad.id_espacio)}</span>
                  </div>

                  <div className="crud-list__actions">
                    <button type="button" onClick={() => handleEdit(actividad)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(actividad.id_actividad)}>
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : null}
        </CrudCard>
      </section>
    </PageShell>
  )
}

export default ActividadesPage