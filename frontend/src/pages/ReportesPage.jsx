import PageShell from '../components/layout/PageShell'

function ReportesPage() {
  return (
    <PageShell
      eyebrow="Análisis"
      title="Reportes"
      description="Espacio reservado para métricas y consultas consolidadas del sistema."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          El módulo de reportes se deja aislado para sumar indicadores sin mezclarlo con la
          navegación operativa.
        </p>
      </section>
    </PageShell>
  )
}

export default ReportesPage