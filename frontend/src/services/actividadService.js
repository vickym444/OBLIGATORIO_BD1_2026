import { request } from './apiClient'

export function listarActividades() {
  return request('/actividades')
}

export function obtenerActividad(idActividad) {
  return request(`/actividades/${idActividad}`)
}

export function crearActividad(actividad) {
  return request('/actividades', {
    method: 'POST',
    body: JSON.stringify(actividad),
  })
}

export function actualizarActividad(idActividad, actividad) {
  return request(`/actividades/${idActividad}`, {
    method: 'PUT',
    body: JSON.stringify(actividad),
  })
}

export function eliminarActividad(idActividad) {
  return request(`/actividades/${idActividad}`, {
    method: 'DELETE',
  })
}