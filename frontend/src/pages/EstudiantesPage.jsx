import { useEffect, useState } from 'react'
import PageShell from '../components/layout/PageShell'
import { listarEstudiantes } from '../services/estudianteService'

function EstudiantesPage() {
  const [estudiantes, setEstudiantes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function cargarEstudiantes() {
      try {
        setIsLoading(true)
        setError('')

        const response = await listarEstudiantes()
        const data = response?.data ?? []

        if (isMounted) {
          setEstudiantes(data)
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
  }, [])

  return (
    <PageShell
      eyebrow="Catálogo"
      title="Estudiantes"
      description="Base visual para administrar estudiantes sin asumir formularios o campos aún no definidos."
    >
      <section className="panel">
        <h2>Listado de estudiantes</h2>

        {isLoading ? <p>Cargando estudiantes...</p> : null}

        {!isLoading && error ? <p>{error}</p> : null}

        {!isLoading && !error && estudiantes.length === 0 ? (
          <p>No hay estudiantes cargados.</p>
        ) : null}

        {!isLoading && !error && estudiantes.length > 0 ? (
          <ul className="placeholder-list">
            {estudiantes.map((estudiante) => (
              <li key={estudiante.id_estudiante}>
                <span>
                  {estudiante.nombre} {estudiante.apellido}
                </span>
                <span>{estudiante.documento}</span>
              </li>
            ))}
          </ul>
        ) : null}
      </section>
    </PageShell>
  )
}

export default EstudiantesPage