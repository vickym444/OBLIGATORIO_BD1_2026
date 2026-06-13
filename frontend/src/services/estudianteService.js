const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  const hasBody = response.status !== 204
  const payload = hasBody ? await response.json().catch(() => null) : null

  if (!response.ok) {
    const message = payload?.detail ?? payload?.message ?? 'Error al comunicarse con el backend'
    throw new Error(message)
  }

  return payload
}

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