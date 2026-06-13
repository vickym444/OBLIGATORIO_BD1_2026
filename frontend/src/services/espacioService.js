import { request } from './apiClient'

export function listarEspacios() {
  return request('/espacios')
}

export function obtenerEspacio(idEspacio) {
  return request(`/espacios/${idEspacio}`)
}

export function crearEspacio(espacio) {
  return request('/espacios', {
    method: 'POST',
    body: JSON.stringify(espacio),
  })
}

export function actualizarEspacio(idEspacio, espacio) {
  return request(`/espacios/${idEspacio}`, {
    method: 'PUT',
    body: JSON.stringify(espacio),
  })
}

export function eliminarEspacio(idEspacio) {
  return request(`/espacios/${idEspacio}`, {
    method: 'DELETE',
  })
}