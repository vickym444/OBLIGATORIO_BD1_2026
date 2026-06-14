import { request } from './apiClient'

export function inscribirseAPractica(idPractica, idEstudiante, fechaInscripcion) {
  return request('/inscripciones', {
    method: 'POST',
    body: JSON.stringify({
      fecha_inscripcion: fechaInscripcion,
      id_estudiante: idEstudiante,
      id_practica: idPractica,
    }),
  })
}

export function listarMisInscripciones() {
  return request('/inscripciones/mias')
}

export function listarInscripcionesAdmin({ fechaDesde, fechaHasta } = {}) {
  const params = new URLSearchParams()

  if (fechaDesde) {
    params.set('fecha_desde', fechaDesde)
  }

  if (fechaHasta) {
    params.set('fecha_hasta', fechaHasta)
  }

  const query = params.toString()
  return request(`/inscripciones${query ? `?${query}` : ''}`)
}

export function cancelarInscripcion(idInscripcion, fechaBaja) {
  return request(`/inscripciones/${idInscripcion}`, {
    method: 'DELETE',
    body: JSON.stringify({ fecha_baja: fechaBaja }),
  })
}
