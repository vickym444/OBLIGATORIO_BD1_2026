import PageShell from '../components/layout/PageShell'

const dashboardCards = [
  {
    label: 'Estado general',
    title: 'Base estructural lista',
    text: 'El layout principal y las rutas ya están montados para conectar datos reales.',
  },
  {
    label: 'Catálogos',
    title: 'Estudiantes, disciplinas y espacios',
    text: 'Los módulos coinciden con las entidades presentes en el backend y el esquema SQL.',
  },
  {
    label: 'Gestión operativa',
    title: 'Actividades, inscripciones y asistencias',
    text: 'La navegación deja preparados los flujos que más adelante se conectarán con servicios.',
  },
  {
    label: 'Reportes',
    title: 'Vista separada para análisis',
    text: 'El módulo queda aislado para sumar métricas o filtros sin tocar el layout base.',
  },
]

function DashboardPage() {
  return (
    <PageShell
      eyebrow="Inicio"
      title="Dashboard"
      description="Punto de entrada del sistema de gestión de actividades deportivas universitarias."
    >
      <div className="dashboard-grid">
        {dashboardCards.map((card) => (
          <article key={card.title} className="info-card">
            <p className="info-card__label">{card.label}</p>
            <h2 className="info-card__title">{card.title}</h2>
            <p className="info-card__text">{card.text}</p>
          </article>
        ))}
      </div>

      <section className="panel">
        <h2>Próximo paso</h2>
        <p>
          Cuando empecemos a conectar datos reales, cada módulo podrá consumir las entidades
          ya definidas en el backend sin cambiar esta estructura base.
        </p>
      </section>
    </PageShell>
  )
}

export default DashboardPage