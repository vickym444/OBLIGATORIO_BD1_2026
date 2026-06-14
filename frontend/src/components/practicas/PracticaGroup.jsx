import PracticaListItem from './PracticaListItem'

function PracticaGroup({ fecha, practicas, getActividadNombre, getDetalleActividad }) {
  return (
    <section className="practice-group">
      <header className="practice-group__header">
        <h3>{fecha}</h3>
        <span>{practicas.length} práctica(s)</span>
      </header>

      <ul className="practice-list">
        {practicas.map((practica) => (
          <PracticaListItem
            key={practica.id_practica}
            practica={practica}
            actividadNombre={getActividadNombre(practica.id_actividad)}
            detalleActividad={getDetalleActividad(practica.id_actividad)}
          />
        ))}
      </ul>
    </section>
  )
}

export default PracticaGroup