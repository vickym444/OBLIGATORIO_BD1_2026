function PracticaListItem({ practica, actividadNombre, detalleActividad }) {
  return (
    <li className="practice-list__item">
      <div>
        <strong>{actividadNombre}</strong>
        <span>ID práctica {practica.id_practica}</span>
        <span>ID actividad {practica.id_actividad}</span>
        <span>{practica.fecha}</span>
        {detalleActividad ? <span>{detalleActividad}</span> : null}
      </div>

      <div className="practice-list__badge">Activa</div>
    </li>
  )
}

export default PracticaListItem