import { useEffect, useMemo, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import PaginationControls from '../components/common/PaginationControls'
import { listarCarreras } from '../services/carreraService'
import {
  actualizarEstudiante,
  crearEstudiante,
  eliminarEstudiante,
  listarEstudiantes,
} from '../services/estudianteService'

const initialForm = {
  documento: '',
  nombre: '',
  apellido: '',
  email: '',
  id_carrera: '',
}

const ITEMS_PER_PAGE = 10

function EstudiantesPage() {
  const [estudiantes, setEstudiantes] = useState([])
  const [carreras, setCarreras] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [formValues, setFormValues] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)
  const [soloCon3Inasistencias, setSoloCon3Inasistencias] = useState(false)
  const [textoBusqueda, setTextoBusqueda] = useState('')
  const [paginaActual, setPaginaActual] = useState(1)

  useEffect(() => {
    let isMounted = true

    async function cargarEstudiantes() {
      try {
        setIsLoading(true)
        setError('')

        const [estudiantesResponse, carrerasResponse] = await Promise.all([
          listarEstudiantes(soloCon3Inasistencias),
          listarCarreras(),
        ])
        const data = estudiantesResponse?.data ?? []

        if (isMounted) {
          setEstudiantes(data)
          setCarreras(carrerasResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar los estudiantes')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    cargarEstudiantes()

    return () => {
      isMounted = false
    }
  }, [soloCon3Inasistencias])

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

  async function reloadEstudiantes() {
    const response = await listarEstudiantes(soloCon3Inasistencias)
    setEstudiantes(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const documento = formValues.documento.trim()
    const nombre = formValues.nombre.trim()
    const apellido = formValues.apellido.trim()
    const email = formValues.email.trim()
    const idCarrera = Number(formValues.id_carrera)

    if (!documento) {
      setError('El documento del estudiante es obligatorio')
      return
    }

    if (!nombre) {
      setError('El nombre del estudiante es obligatorio')
      return
    }

    if (!apellido) {
      setError('El apellido del estudiante es obligatorio')
      return
    }

    if (!email) {
      setError('El email del estudiante es obligatorio')
      return
    }

    if (!idCarrera) {
      setError('Debes seleccionar una carrera')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      const payload = {
        documento,
        nombre,
        apellido,
        email,
        id_carrera: idCarrera,
      }

      if (editingId) {
        const current = estudiantes.find((item) => item.id_estudiante === editingId)
        await actualizarEstudiante(editingId, {
          ...payload,
          activo: current?.activo ?? 1,
        })
      } else {
        await crearEstudiante(payload)
      }

      await reloadEstudiantes()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar el estudiante')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(estudiante) {
    setEditingId(estudiante.id_estudiante)
    setFormValues({
      documento: estudiante.documento,
      nombre: estudiante.nombre,
      apellido: estudiante.apellido,
      email: estudiante.email,
      id_carrera: String(estudiante.id_carrera),
    })
    setError('')
  }

  async function handleDelete(idEstudiante) {
    const shouldDelete = window.confirm('¿Eliminar este estudiante? Se marcará como inactivo.')
    if (!shouldDelete) {
      return
    }

    try {
      setError('')
      await eliminarEstudiante(idEstudiante)
      await reloadEstudiantes()

      if (editingId === idEstudiante) {
        resetForm()
      }
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar el estudiante')
    }
  }

  function getCarreraNombre(idCarrera) {
    const carrera = carreras.find((item) => item.id_carrera === idCarrera)
    return carrera?.nombre ?? `Carrera ${idCarrera}`
  }

  const estudiantesFiltrados = useMemo(() => {
    const query = textoBusqueda.trim().toLowerCase()

    if (!query) {
      return estudiantes
    }

    return estudiantes.filter((estudiante) => {
      const nombreCompleto = `${estudiante.nombre ?? ''} ${estudiante.apellido ?? ''}`.toLowerCase()
      const documento = String(estudiante.documento ?? '').toLowerCase()
      const email = String(estudiante.email ?? '').toLowerCase()
      const carreraItem = carreras.find((item) => item.id_carrera === estudiante.id_carrera)
      const carrera = (carreraItem?.nombre ?? `Carrera ${estudiante.id_carrera}`).toLowerCase()
      const id = String(estudiante.id_estudiante ?? '')

      return (
        nombreCompleto.includes(query)
        || documento.includes(query)
        || email.includes(query)
        || carrera.includes(query)
        || id.includes(query)
      )
    })
  }, [estudiantes, textoBusqueda, carreras])

  const totalPaginas = useMemo(
    () => Math.max(1, Math.ceil(estudiantesFiltrados.length / ITEMS_PER_PAGE)),
    [estudiantesFiltrados],
  )

  const paginaActualSegura = Math.min(paginaActual, totalPaginas)

  const estudiantesPaginados = useMemo(() => {
    const start = (paginaActualSegura - 1) * ITEMS_PER_PAGE
    return estudiantesFiltrados.slice(start, start + ITEMS_PER_PAGE)
  }, [estudiantesFiltrados, paginaActualSegura])

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Estudiantes"
      description="ABM de estudiantes conectado al backend real, con carrera asociada y borrado lógico."
    >
      <section className="panel crud-grid">
        <CrudCard title={editingId ? 'Editar estudiante' : 'Nuevo estudiante'}>
          <form className="crud-form" onSubmit={handleSubmit}>
            <div className="crud-form__grid">
              <CrudField
                label="Documento"
                name="documento"
                value={formValues.documento}
                onChange={handleChange}
                placeholder="Ej.: 4.567.890"
              />

              <CrudField
                label="Email"
                name="email"
                value={formValues.email}
                onChange={handleChange}
                type="email"
                placeholder="Ej.: alumno@correo.com"
              />

              <CrudField
                label="Nombre"
                name="nombre"
                value={formValues.nombre}
                onChange={handleChange}
                placeholder="Ej.: Ana"
              />

              <CrudField
                label="Apellido"
                name="apellido"
                value={formValues.apellido}
                onChange={handleChange}
                placeholder="Ej.: Pérez"
              />

              <CrudField
                label="Carrera"
                name="id_carrera"
                value={formValues.id_carrera}
                onChange={handleChange}
                as="select"
                placeholder="Seleccionar carrera"
                options={carreras.map((carrera) => ({
                  value: carrera.id_carrera,
                  label: carrera.nombre,
                }))}
                className="crud-field--full"
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

        <CrudCard title="Listado de estudiantes">
          <CrudField
            label="Buscar estudiante"
            name="buscar_estudiante"
            value={textoBusqueda}
            onChange={(event) => setTextoBusqueda(event.target.value)}
            placeholder="Buscar por nombre, apellido, documento, email, carrera o ID"
            className="crud-field--full"
          />

          <label className="practice-sort-toggle">
            <input
              type="checkbox"
              checked={soloCon3Inasistencias}
              onChange={(event) => setSoloCon3Inasistencias(event.target.checked)}
            />
            <span>Mostrar únicamente estudiantes con 3 o más inasistencias</span>
          </label>

          {isLoading ? <p>Cargando estudiantes...</p> : null}

          {!isLoading && !error && estudiantes.length === 0 ? <p>No hay estudiantes cargados.</p> : null}

          {!isLoading && !error && estudiantes.length > 0 && estudiantesFiltrados.length === 0 ? (
            <p>No hay estudiantes que coincidan con la búsqueda.</p>
          ) : null}

          {!isLoading && estudiantesFiltrados.length > 0 ? (
            <ul className="crud-list">
              {estudiantesPaginados.map((estudiante) => (
                <li key={estudiante.id_estudiante} className="crud-list__item">
                  <div>
                    <strong>
                      {estudiante.nombre} {estudiante.apellido}
                    </strong>
                    <span>ID {estudiante.id_estudiante}</span>
                    <span>{estudiante.documento}</span>
                    <span>{estudiante.email}</span>
                    <span>{getCarreraNombre(estudiante.id_carrera)}</span>
                    <span>Inasistencias acumuladas: {estudiante.total_inasistencias ?? 0}</span>
                  </div>

                  <div className="crud-list__actions">
                    <button type="button" onClick={() => handleEdit(estudiante)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(estudiante.id_estudiante)}>
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : null}

          {!isLoading && estudiantesFiltrados.length > ITEMS_PER_PAGE ? (
            <PaginationControls
              currentPage={paginaActualSegura}
              totalPages={totalPaginas}
              onPageChange={setPaginaActual}
              itemLabel="estudiantes"
              totalItems={estudiantesFiltrados.length}
            />
          ) : null}
        </CrudCard>
      </section>
    </PageShell>
  )
}

export default EstudiantesPage