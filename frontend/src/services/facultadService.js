import { request } from './apiClient'

export function listarFacultades() {
  return request('/facultades')
}

export function obtenerFacultad(idFacultad) {
  return request(`/facultades/${idFacultad}`)
}

export function crearFacultad(facultad) {
  return request('/facultades', {
    method: 'POST',
    body: JSON.stringify(facultad),
  })
}

export function actualizarFacultad(idFacultad, facultad) {
  return request(`/facultades/${idFacultad}`, {
    method: 'PUT',
    body: JSON.stringify(facultad),
  })
}

export function eliminarFacultad(idFacultad) {
  return request(`/facultades/${idFacultad}`, {
    method: 'DELETE',
  })
}