import PageShell from '../components/layout/PageShell'

function ActividadesPage() {
  return (
    <PageShell
      eyebrow="Operación"
      title="Actividades"
      description="Pantalla base para mostrar y administrar las actividades deportivas."
    >
      <section className="panel">
        <h2>Vista base</h2>
        <p>
          Este módulo ya está enrutado y listo para conectar con la entidad actividad
          existente en el backend.
        </p>
      </section>
    </PageShell>
  )
}

export default ActividadesPage