function PracticaListItem({
  practica,
  actividadNombre,
  detalleActividad,
  estadoInscripcion,
  onInscribir,
  isInscribiendo = false,
  canInscribir = true,
}) {
  const etiquetaEstado =
    estadoInscripcion?.estado === 'confirmada'
      ? 'Ya inscripto'
      : estadoInscripcion?.estado === 'en_espera'
        ? 'En espera'
        : 'Activa'

  return (
    <li className="practice-list__item">
      <div>
        <strong>{actividadNombre}</strong>
        <span>ID práctica {practica.id_practica}</span>
        <span>ID actividad {practica.id_actividad}</span>
        <span>{practica.fecha}</span>
        {detalleActividad ? <span>{detalleActividad}</span> : null}
      </div>

      <div className="practice-list__side">
        <div className={`practice-list__badge practice-list__badge--${estadoInscripcion?.estado || 'disponible'}`}>
          {etiquetaEstado}
        </div>

        {onInscribir ? (
          <button
            type="button"
            className="practice-list__button"
            onClick={() => onInscribir(practica)}
            disabled={!canInscribir || isInscribiendo}
          >
            {isInscribiendo ? 'Inscribiendo...' : 'Inscribirme'}
          </button>
        ) : null}
      </div>
    </li>
  )
}

export default PracticaListItem