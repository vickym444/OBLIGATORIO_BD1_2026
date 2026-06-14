import { request } from './apiClient'

export function listarUsuarios() {
  return request('/usuarios')
}

export function obtenerUsuario(idUsuario) {
  return request(`/usuarios/${idUsuario}`)
}

export function crearUsuario(usuario) {
  return request('/usuarios', {
    method: 'POST',
    body: JSON.stringify(usuario),
  })
}

export function actualizarUsuario(idUsuario, usuario) {
  return request(`/usuarios/${idUsuario}`, {
    method: 'PUT',
    body: JSON.stringify(usuario),
  })
}

export function eliminarUsuario(idUsuario) {
  return request(`/usuarios/${idUsuario}`, {
    method: 'DELETE',
  })
}