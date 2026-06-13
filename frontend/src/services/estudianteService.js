import { request } from './apiClient'

export function listarEstudiantes() {
  return request('/estudiantes')
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