import PageShell from '../components/layout/PageShell'

function DisciplinasPage() {
  return (
    <PageShell
      eyebrow="Catálogo"
      title="Disciplinas"
      description="Estructura mínima para gestionar las disciplinas deportivas registradas en la base."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          Este módulo queda listo para listar y editar disciplinas cuando se conecte con las
          consultas reales del backend.
        </p>
      </section>
    </PageShell>
  )
}

export default DisciplinasPage