import { useEffect, useMemo, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import PaginationControls from '../components/common/PaginationControls'
import {
  actualizarFacultad,
  crearFacultad,
  eliminarFacultad,
  listarFacultades,
} from '../services/facultadService'

const initialForm = {
  nombre: '',
}

const ITEMS_PER_PAGE = 10

function FacultadesPage() {
  const [facultades, setFacultades] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [formValues, setFormValues] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)
  const [paginaActual, setPaginaActual] = useState(1)

  useEffect(() => {
    let isMounted = true

    async function cargarFacultades() {
      try {
        setIsLoading(true)
        setError('')

        const response = await listarFacultades()
        const data = response?.data ?? []

        if (isMounted) {
          setFacultades(data)
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las facultades')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarFacultades()

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

  async function reloadFacultades() {
    const response = await listarFacultades()
    setFacultades(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nombre = formValues.nombre.trim()
    if (!nombre) {
      setError('El nombre de la facultad es obligatorio')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      if (editingId) {
        await actualizarFacultad(editingId, { nombre })
      } else {
        await crearFacultad({ nombre })
      }

      await reloadFacultades()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar la facultad')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(facultad) {
    setEditingId(facultad.id_facultad)
    setFormValues({ nombre: facultad.nombre })
    setError('')
  }

  async function handleDelete(idFacultad) {
    const shouldDelete = window.confirm('¿Eliminar esta facultad? Se marcará como inactiva.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarFacultad(idFacultad)
      await reloadFacultades()

      if (editingId === idFacultad) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar la facultad')
    }
  }

  const totalPaginas = useMemo(
    () => Math.max(1, Math.ceil(facultades.length / ITEMS_PER_PAGE)),
    [facultades],
  )

  const paginaActualSegura = Math.min(paginaActual, totalPaginas)

  const facultadesPaginadas = useMemo(() => {
    const start = (paginaActualSegura - 1) * ITEMS_PER_PAGE
    return facultades.slice(start, start + ITEMS_PER_PAGE)
  }, [facultades, paginaActualSegura])

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Facultades"
      description="ABM base de facultades conectado al backend real, sin datos simulados."
    >
      <section className="panel faculty-grid">
        <div className="faculty-card">
          <h2>{editingId ? 'Editar facultad' : 'Nueva facultad'}</h2>

          <form className="faculty-form" onSubmit={handleSubmit}>
            <label className="faculty-form__field">
              <span>Nombre</span>
              <input
                type="text"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Facultad de Ingeniería"
              />
            </label>

            <div className="faculty-form__actions">
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

          {error ? <p className="faculty-message faculty-message--error">{error}</p> : null}
        </div>

        <div className="faculty-card">
          <h2>Listado de facultades</h2>

          {isLoading ? <p>Cargando facultades...</p> : null}

          {!isLoading && !error && facultades.length === 0 ? (
            <p>No hay facultades cargadas.</p>
          ) : null}

          {!isLoading && facultades.length > 0 ? (
            <ul className="faculty-list">
              {facultadesPaginadas.map((facultad) => (
                <li key={facultad.id_facultad} className="faculty-list__item">
                  <div>
                    <strong>{facultad.nombre}</strong>
                    <span>ID {facultad.id_facultad}</span>
                  </div>

                  <div className="faculty-list__actions">
                    <button type="button" onClick={() => handleEdit(facultad)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(facultad.id_facultad)}>
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : null}

          {!isLoading && facultades.length > ITEMS_PER_PAGE ? (
            <PaginationControls
              currentPage={paginaActualSegura}
              totalPages={totalPaginas}
              onPageChange={setPaginaActual}
              itemLabel="facultades"
              totalItems={facultades.length}
            />
          ) : null}
        </div>
      </section>
    </PageShell>
  )
}

export default FacultadesPage