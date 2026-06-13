import { useEffect, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import { listarFacultades } from '../services/facultadService'
import {
  actualizarCarrera,
  crearCarrera,
  eliminarCarrera,
  listarCarreras,
} from '../services/carreraService'

const initialForm = {
  nombre: '',
  id_facultad: '',
}

function CarrerasPage() {
  const [carreras, setCarreras] = useState([])
  const [facultades, setFacultades] = useState([])
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

        const [carrerasResponse, facultadesResponse] = await Promise.all([
          listarCarreras(),
          listarFacultades(),
        ])

        if (isMounted) {
          setCarreras(carrerasResponse?.data ?? [])
          setFacultades(facultadesResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las carreras')
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

  async function reloadCarreras() {
    const response = await listarCarreras()
    setCarreras(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nombre = formValues.nombre.trim()
    const idFacultad = Number(formValues.id_facultad)

    if (!nombre) {
      setError('El nombre de la carrera es obligatorio')
      return
    }

    if (!idFacultad) {
      setError('Debes seleccionar una facultad')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      const payload = {
        nombre,
        id_facultad: idFacultad,
        activo: 1,
      }

      if (editingId) {
        await actualizarCarrera(editingId, payload)
      } else {
        await crearCarrera({ nombre, id_facultad: idFacultad })
      }

      await reloadCarreras()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar la carrera')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(carrera) {
    setEditingId(carrera.id_carrera)
    setFormValues({
      nombre: carrera.nombre,
      id_facultad: String(carrera.id_facultad),
    })
    setError('')
  }

  async function handleDelete(idCarrera) {
    const shouldDelete = window.confirm('¿Eliminar esta carrera? Se marcará como inactiva.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarCarrera(idCarrera)
      await reloadCarreras()

      if (editingId === idCarrera) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar la carrera')
    }
  }

  function getFacultadNombre(idFacultad) {
    const facultad = facultades.find((item) => item.id_facultad === idFacultad)
    return facultad?.nombre ?? `Facultad ${idFacultad}`
  }

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Carreras"
      description="ABM de carreras conectado al backend real, asociado a facultades activas."
    >
      <section className="panel career-grid">
        <div className="career-card">
          <h2>{editingId ? 'Editar carrera' : 'Nueva carrera'}</h2>

          <form className="career-form" onSubmit={handleSubmit}>
            <label className="career-form__field">
              <span>Nombre</span>
              <input
                type="text"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Ingeniería en Sistemas"
              />
            </label>

            <label className="career-form__field">
              <span>Facultad</span>
              <select name="id_facultad" value={formValues.id_facultad} onChange={handleChange}>
                <option value="">Seleccionar facultad</option>
                {facultades.map((facultad) => (
                  <option key={facultad.id_facultad} value={facultad.id_facultad}>
                    {facultad.nombre}
                  </option>
                ))}
              </select>
            </label>

            <div className="career-form__actions">
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

          {error ? <p className="career-message career-message--error">{error}</p> : null}
        </div>

        <div className="career-card">
          <h2>Listado de carreras</h2>

          {isLoading ? <p>Cargando carreras...</p> : null}

          {!isLoading && !error && carreras.length === 0 ? <p>No hay carreras cargadas.</p> : null}

          {!isLoading && carreras.length > 0 ? (
            <ul className="career-list">
              {carreras.map((carrera) => (
                <li key={carrera.id_carrera} className="career-list__item">
                  <div>
                    <strong>{carrera.nombre}</strong>
                    <span>ID {carrera.id_carrera}</span>
                    <span>{getFacultadNombre(carrera.id_facultad)}</span>
                  </div>

                  <div className="career-list__actions">
                    <button type="button" onClick={() => handleEdit(carrera)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(carrera.id_carrera)}>
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      </section>
    </PageShell>
  )
}

export default CarrerasPage