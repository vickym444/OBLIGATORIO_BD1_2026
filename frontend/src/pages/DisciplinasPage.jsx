import { useEffect, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import {
  actualizarDisciplina,
  crearDisciplina,
  eliminarDisciplina,
  listarDisciplinas,
} from '../services/disciplinaService'

const initialForm = {
  nombre: '',
  descripcion: '',
}

function DisciplinasPage() {
  const [disciplinas, setDisciplinas] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [formValues, setFormValues] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)

  useEffect(() => {
    let isMounted = true

    async function cargarDisciplinas() {
      try {
        setIsLoading(true)
        setError('')

        const response = await listarDisciplinas()
        const data = response?.data ?? []

        if (isMounted) {
          setDisciplinas(data)
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar las disciplinas')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarDisciplinas()

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

  async function reloadDisciplinas() {
    const response = await listarDisciplinas()
    setDisciplinas(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nombre = formValues.nombre.trim()
    const descripcion = formValues.descripcion.trim()

    if (!nombre) {
      setError('El nombre de la disciplina es obligatorio')
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
        const current = disciplinas.find((item) => item.id_disciplina === editingId)
        await actualizarDisciplina(editingId, {
          ...payload,
          activo: current?.activo ?? 1,
        })
      } else {
        await crearDisciplina(payload)
      }

      await reloadDisciplinas()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar la disciplina')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(disciplina) {
    setEditingId(disciplina.id_disciplina)
    setFormValues({
      nombre: disciplina.nombre,
      descripcion: disciplina.descripcion ?? '',
    })
    setError('')
  }

  async function handleDelete(idDisciplina) {
    const shouldDelete = window.confirm('¿Eliminar esta disciplina? Se marcará como inactiva.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarDisciplina(idDisciplina)
      await reloadDisciplinas()

      if (editingId === idDisciplina) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar la disciplina')
    }
  }

  function getDescripcion(disciplina) {
    return disciplina.descripcion?.trim() || 'Sin descripción'
  }

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Disciplinas"
      description="ABM de disciplinas conectado al backend real, con listado, alta, edición y borrado lógico."
    >
      <section className="panel faculty-grid">
        <div className="faculty-card">
          <h2>{editingId ? 'Editar disciplina' : 'Nueva disciplina'}</h2>

          <form className="faculty-form" onSubmit={handleSubmit}>
            <label className="faculty-form__field">
              <span>Nombre</span>
              <input
                type="text"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Futbol"
              />
            </label>

            <label className="faculty-form__field">
              <span>Descripción</span>
              <textarea
                name="descripcion"
                value={formValues.descripcion}
                onChange={handleChange}
                placeholder="Ej.: Deporte de equipo"
                rows="4"
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
          <h2>Listado de disciplinas</h2>

          {isLoading ? <p>Cargando disciplinas...</p> : null}

          {!isLoading && !error && disciplinas.length === 0 ? (
            <p>No hay disciplinas cargadas.</p>
          ) : null}

          {!isLoading && disciplinas.length > 0 ? (
            <ul className="faculty-list">
              {disciplinas.map((disciplina) => (
                <li key={disciplina.id_disciplina} className="faculty-list__item">
                  <div>
                    <strong>{disciplina.nombre}</strong>
                    <span>ID {disciplina.id_disciplina}</span>
                    <span>{getDescripcion(disciplina)}</span>
                  </div>

                  <div className="faculty-list__actions">
                    <button type="button" onClick={() => handleEdit(disciplina)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(disciplina.id_disciplina)}>
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

export default DisciplinasPage