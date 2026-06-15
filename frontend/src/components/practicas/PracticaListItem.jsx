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

  const inscriptosConfirmados = practica.inscriptos_confirmados ?? 0
  const cupoMaximo = practica.cupo_maximo ?? 0
  const porcentajeInscriptos =
    cupoMaximo > 0 ? Math.round((inscriptosConfirmados / cupoMaximo) * 100) : 0

  function formatHour(value) {
    if (value === null || value === undefined || value === '') {
      return ''
    }

    if (typeof value === 'number') {
      const totalSeconds = Math.max(0, Math.floor(value))
      const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0')
      const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0')
      return `${hours}:${minutes}`
    }

    const text = String(value)
    const match = text.match(/^(\d{1,2}):(\d{2})/)
    if (match) {
      const hours = match[1].padStart(2, '0')
      const minutes = match[2]
      return `${hours}:${minutes}`
    }

    return text
  }

  const horaInicio = formatHour(practica.hora_inicio)
  const horaFin = formatHour(practica.hora_fin)

  return (
    <li className="practice-list__item">
      <div>
        <strong>{actividadNombre}</strong>
        <span>ID práctica {practica.id_practica}</span>
        <span>ID actividad {practica.id_actividad}</span>
        <span>
          {practica.fecha}
          {horaInicio && horaFin ? ` · ${horaInicio} a ${horaFin}` : ''}
        </span>
        <span className="practice-list__capacity">
          {inscriptosConfirmados}/{cupoMaximo} ({porcentajeInscriptos}%)
        </span>
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