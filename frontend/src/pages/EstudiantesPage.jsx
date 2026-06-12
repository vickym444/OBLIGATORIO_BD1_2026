import PageShell from '../components/layout/PageShell'

function EstudiantesPage() {
  return (
    <PageShell
      eyebrow="Catálogo"
      title="Estudiantes"
      description="Base visual para administrar estudiantes sin asumir formularios o campos aún no definidos."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          Aquí conectaremos el listado y las acciones sobre la entidad estudiante cuando se
          definan los casos de uso concretos.
        </p>
      </section>
    </PageShell>
  )
}

export default EstudiantesPage