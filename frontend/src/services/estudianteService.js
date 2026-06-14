import { request } from './apiClient'

export function listarEstudiantes(soloCon3Inasistencias = false) {
  const params = new URLSearchParams()

  if (soloCon3Inasistencias) {
    params.set('solo_con_3_inasistencias', 'true')
  }

  const query = params.toString()
  return request(`/estudiantes${query ? `?${query}` : ''}`)
}

export function obtenerEstudiante(idEstudiante) {
  return request(`/estudiantes/${idEstudiante}`)
}

export function crearEstudiante(estudiante) {
  return request('/estudiantes', {
    method: 'POST',
    body: JSON.stringify(estudiante),
  })
}

export function actualizarEstudiante(idEstudiante, estudiante) {
  return request(`/estudiantes/${idEstudiante}`, {
    method: 'PUT',
    body: JSON.stringify(estudiante),
  })
}

export function eliminarEstudiante(idEstudiante) {
  return request(`/estudiantes/${idEstudiante}`, {
    method: 'DELETE',
  })
}