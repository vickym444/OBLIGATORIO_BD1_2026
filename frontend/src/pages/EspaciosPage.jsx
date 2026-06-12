import PageShell from '../components/layout/PageShell'

function EspaciosPage() {
  return (
    <PageShell
      eyebrow="Catálogo"
      title="Espacios"
      description="Base de pantalla para administrar los espacios vinculados a las actividades."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          La pantalla queda preparada para mostrar disponibilidad, capacidad y relación con
          actividades cuando se implementen los datos.
        </p>
      </section>
    </PageShell>
  )
}

export default EspaciosPage