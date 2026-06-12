import PageShell from '../components/layout/PageShell'

function InscripcionesPage() {
  return (
    <PageShell
      eyebrow="Operación"
      title="Inscripciones"
      description="Base para gestionar la relación entre estudiantes y prácticas o actividades."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          En esta pantalla se integrarán las altas, bajas y estados de las inscripciones
          cuando se defina el flujo de negocio.
        </p>
      </section>
    </PageShell>
  )
}

export default InscripcionesPage