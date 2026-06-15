import { useEffect, useMemo, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import PaginationControls from '../components/common/PaginationControls'
import {
  actualizarEspacio,
  crearEspacio,
  eliminarEspacio,
  listarEspacios,
} from '../services/espacioService'

const initialForm = {
  nombre: '',
  descripcion: '',
}

const ITEMS_PER_PAGE = 10

function EspaciosPage() {
  const [espacios, setEspacios] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [formValues, setFormValues] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)
  const [paginaActual, setPaginaActual] = useState(1)

  useEffect(() => {
    let isMounted = true

    async function cargarEspacios() {
      try {
        setIsLoading(true)
        setError('')

        const response = await listarEspacios()
        const data = response?.data ?? []

        if (isMounted) {
          setEspacios(data)
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar los espacios')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarEspacios()

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

  async function reloadEspacios() {
    const response = await listarEspacios()
    setEspacios(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nombre = formValues.nombre.trim()
    const descripcion = formValues.descripcion.trim()

    if (!nombre) {
      setError('El nombre del espacio es obligatorio')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      const payload = {
        nombre,
        descripcion: descripcion || null,
      }

      if (editingId) {
        await actualizarEspacio(editingId, { ...payload, activo: 1 })
      } else {
        await crearEspacio(payload)
      }

      await reloadEspacios()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar el espacio')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(espacio) {
    setEditingId(espacio.id_espacio)
    setFormValues({
      nombre: espacio.nombre,
      descripcion: espacio.descripcion ?? '',
    })
    setError('')
  }

  async function handleDelete(idEspacio) {
    const shouldDelete = window.confirm('¿Eliminar este espacio? Se marcará como inactivo.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarEspacio(idEspacio)
      await reloadEspacios()

      if (editingId === idEspacio) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar el espacio')
    }
  }

  function getDescripcion(espacio) {
    return espacio.descripcion?.trim() || 'Sin descripción'
  }

  const totalPaginas = useMemo(
    () => Math.max(1, Math.ceil(espacios.length / ITEMS_PER_PAGE)),
    [espacios],
  )

  const paginaActualSegura = Math.min(paginaActual, totalPaginas)

  const espaciosPaginados = useMemo(() => {
    const start = (paginaActualSegura - 1) * ITEMS_PER_PAGE
    return espacios.slice(start, start + ITEMS_PER_PAGE)
  }, [espacios, paginaActualSegura])

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Espacios"
      description="ABM de espacios conectado al backend real, con borrado lógico y lista de activos."
    >
      <section className="panel space-grid">
        <div className="space-card">
          <h2>{editingId ? 'Editar espacio' : 'Nuevo espacio'}</h2>

          <form className="space-form" onSubmit={handleSubmit}>
            <label className="space-form__field">
              <span>Nombre</span>
              <input
                type="text"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Aula 101"
              />
            </label>

            <label className="space-form__field">
              <span>Descripción</span>
              <textarea
                name="descripcion"
                value={formValues.descripcion}
                onChange={handleChange}
                placeholder="Ej.: Aula para 40 estudiantes"
                rows="4"
              />
            </label>

            <div className="space-form__actions">
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

          {error ? <p className="space-message space-message--error">{error}</p> : null}
        </div>

        <div className="space-card">
          <h2>Listado de espacios</h2>

          {isLoading ? <p>Cargando espacios...</p> : null}

          {!isLoading && !error && espacios.length === 0 ? <p>No hay espacios cargados.</p> : null}

          {!isLoading && espacios.length > 0 ? (
            <ul className="space-list">
              {espaciosPaginados.map((espacio) => (
                <li key={espacio.id_espacio} className="space-list__item">
                  <div>
                    <strong>{espacio.nombre}</strong>
                    <span>ID {espacio.id_espacio}</span>
                    <span>{getDescripcion(espacio)}</span>
                  </div>

                  <div className="space-list__actions">
                    <button type="button" onClick={() => handleEdit(espacio)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(espacio.id_espacio)}>
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : null}

          {!isLoading && espacios.length > ITEMS_PER_PAGE ? (
            <PaginationControls
              currentPage={paginaActualSegura}
              totalPages={totalPaginas}
              onPageChange={setPaginaActual}
              itemLabel="espacios"
              totalItems={espacios.length}
            />
          ) : null}
        </div>
      </section>
    </PageShell>
  )
}

export default EspaciosPage