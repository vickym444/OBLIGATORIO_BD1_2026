import { request } from './apiClient'

export function listarDisciplinas() {
  return request('/disciplinas')
}

export function obtenerDisciplina(idDisciplina) {
  return request(`/disciplinas/${idDisciplina}`)
}

export function crearDisciplina(disciplina) {
  return request('/disciplinas', {
    method: 'POST',
    body: JSON.stringify(disciplina),
  })
}

export function actualizarDisciplina(idDisciplina, disciplina) {
  return request(`/disciplinas/${idDisciplina}`, {
    method: 'PUT',
    body: JSON.stringify(disciplina),
  })
}

export function eliminarDisciplina(idDisciplina) {
  return request(`/disciplinas/${idDisciplina}`, {
    method: 'DELETE',
  })
}