import { request } from './apiClient'

export function listarCarreras() {
  return request('/carreras')
}

export function obtenerCarrera(idCarrera) {
  return request(`/carreras/${idCarrera}`)
}

export function crearCarrera(carrera) {
  return request('/carreras', {
    method: 'POST',
    body: JSON.stringify(carrera),
  })
}

export function actualizarCarrera(idCarrera, carrera) {
  return request(`/carreras/${idCarrera}`, {
    method: 'PUT',
    body: JSON.stringify(carrera),
  })
}

export function eliminarCarrera(idCarrera) {
  return request(`/carreras/${idCarrera}`, {
    method: 'DELETE',
  })
}