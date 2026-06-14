import { useEffect, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import CrudCard from '../components/crud/CrudCard'
import CrudField from '../components/crud/CrudField'
import { listarEstudiantes } from '../services/estudianteService'
import {
  actualizarUsuario,
  crearUsuario,
  eliminarUsuario,
  listarUsuarios,
} from '../services/usuarioService'

const initialForm = {
  username: '',
  password: '',
  rol: 'estudiante',
  id_estudiante: '',
}

function UsuariosPage() {
  const [usuarios, setUsuarios] = useState([])
  const [estudiantes, setEstudiantes] = useState([])
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

        const [usuariosResponse, estudiantesResponse] = await Promise.all([
          listarUsuarios(),
          listarEstudiantes(),
        ])

        if (isMounted) {
          setUsuarios(usuariosResponse?.data ?? [])
          setEstudiantes(estudiantesResponse?.data ?? [])
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'No se pudieron cargar los usuarios')
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
      ...(name === 'rol' && value === 'admin' ? { id_estudiante: '' } : {}),
    }))
  }

  function resetForm() {
    setFormValues(initialForm)
    setEditingId(null)
    setError('')
  }

  async function reloadUsuarios() {
    const response = await listarUsuarios()
    setUsuarios(response?.data ?? [])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const username = formValues.username.trim()
    const password = formValues.password.trim()
    const rol = formValues.rol
    const idEstudiante = rol === 'estudiante' ? Number(formValues.id_estudiante) : null

    if (!username) {
      setError('El username es obligatorio')
      return
    }

    if (!password && !editingId) {
      setError('La contraseña es obligatoria')
      return
    }

    if (rol === 'estudiante' && !idEstudiante) {
      setError('Debes seleccionar un estudiante')
      return
    }

    try {
      setIsSaving(true)
      setError('')

      const payload = {
        username,
        password,
        rol,
        id_estudiante: idEstudiante,
      }

      if (editingId) {
        const current = usuarios.find((item) => item.id_usuario === editingId)
        await actualizarUsuario(editingId, {
          ...payload,
          activo: current?.activo ?? 1,
        })
      } else {
        await crearUsuario(payload)
      }

      await reloadUsuarios()
      resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo guardar el usuario')
    } finally {
      setIsSaving(false)
    }
  }

  function handleEdit(usuario) {
    setEditingId(usuario.id_usuario)
    setFormValues({
      username: usuario.username,
      password: '',
      rol: usuario.rol,
      id_estudiante: usuario.id_estudiante ? String(usuario.id_estudiante) : '',
    })
    setError('')
  }

  async function handleDelete(idUsuario) {
    const shouldDelete = window.confirm('¿Eliminar este usuario? Se marcará como inactivo.')
    if (!shouldDelete) return

    try {
      setError('')
      await eliminarUsuario(idUsuario)
      await reloadUsuarios()
      if (editingId === idUsuario) resetForm()
    } catch (requestError) {
      setError(requestError.message || 'No se pudo eliminar el usuario')
    }
  }

  function getEstudianteNombre(idEstudiante) {
    const estudiante = estudiantes.find((item) => item.id_estudiante === idEstudiante)
    return estudiante ? `${estudiante.nombre} ${estudiante.apellido}` : '-'
  }

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Usuarios"
      description="ABM de usuarios con rol y borrado lógico."
    >
      <section className="panel crud-grid">
        <CrudCard title={editingId ? 'Editar usuario' : 'Nuevo usuario'}>
          <form className="crud-form" onSubmit={handleSubmit}>
            <div className="crud-form__grid">
              <CrudField
                label="Username"
                name="username"
                value={formValues.username}
                onChange={handleChange}
                placeholder="Ej.: vic123"
              />

              <CrudField
                label="Contraseña"
                name="password"
                value={formValues.password}
                onChange={handleChange}
                type="password"
                placeholder={editingId ? 'Dejar vacío para no cambiar' : 'Contraseña'}
              />

              <CrudField
                label="Rol"
                name="rol"
                value={formValues.rol}
                onChange={handleChange}
                as="select"
                options={[
                  { value: 'estudiante', label: 'Estudiante' },
                  { value: 'admin', label: 'Admin' },
                ]}
              />

              {formValues.rol === 'estudiante' ? (
                <CrudField
                  label="Estudiante"
                  name="id_estudiante"
                  value={formValues.id_estudiante}
                  onChange={handleChange}
                  as="select"
                  placeholder="Seleccionar estudiante"
                  options={estudiantes.map((e) => ({
                    value: e.id_estudiante,
                    label: `${e.nombre} ${e.apellido}`,
                  }))}
                  className="crud-field--full"
                />
              ) : null}
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

        <CrudCard title="Listado de usuarios">
          {isLoading ? <p>Cargando usuarios...</p> : null}

          {!isLoading && !error && usuarios.length === 0 ? (
            <p>No hay usuarios cargados.</p>
          ) : null}

          {!isLoading && usuarios.length > 0 ? (
            <ul className="crud-list">
              {usuarios.map((usuario) => (
                <li key={usuario.id_usuario} className="crud-list__item">
                  <div>
                    <strong>{usuario.username}</strong>
                    <span>ID {usuario.id_usuario}</span>
                    <span>{usuario.rol}</span>
                    <span>
                      {usuario.id_estudiante
                        ? getEstudianteNombre(usuario.id_estudiante)
                        : 'Admin'}
                    </span>
                  </div>

                  <div className="crud-list__actions">
                    <button type="button" onClick={() => handleEdit(usuario)}>
                      Editar
                    </button>
                    <button type="button" onClick={() => handleDelete(usuario.id_usuario)}>
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

export default UsuariosPage