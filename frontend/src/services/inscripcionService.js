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

export function listarInscripcionesAdmin({ fechaDesde, fechaHasta, idFacultad, idCarrera, idActividad, idDisciplina } = {}) {
  const params = new URLSearchParams()

  if (fechaDesde) {
    params.set('fecha_desde', fechaDesde)
  }

  if (fechaHasta) {
    params.set('fecha_hasta', fechaHasta)
  }

  if (idFacultad) {
    params.set('id_facultad', idFacultad)
  }

  if (idCarrera) {
    params.set('id_carrera', idCarrera)
  }

  if (idActividad) {
    params.set('id_actividad', idActividad)
  }

  if (idDisciplina) {
    params.set('id_disciplina', idDisciplina)
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
