import PracticaListItem from './PracticaListItem'

function PracticaGroup({
  fecha,
  practicas,
  getActividadNombre,
  getDetalleActividad,
  getEstadoInscripcion,
  onInscribir,
  isInscribiendoId,
  canInscribir,
}) {
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
            estadoInscripcion={getEstadoInscripcion?.(practica.id_practica)}
            onInscribir={onInscribir}
            isInscribiendo={isInscribiendoId === practica.id_practica}
            canInscribir={canInscribir}
          />
        ))}
      </ul>
    </section>
  )
}

export default PracticaGroup