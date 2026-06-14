export const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

let authToken = null

export function setAuthToken(token) {
  authToken = token
}

export function clearAuthToken() {
  authToken = null
}

export async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers ?? {}),
  }

  // Add Bearer token if available
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  })

  const hasBody = response.status !== 204
  const payload = hasBody ? await response.json().catch(() => null) : null

  if (!response.ok) {
    const message = payload?.detail ?? payload?.message ?? 'Error al comunicarse con el backend'
    const error = new Error(message)
    error.status = response.status
    throw error
  }

  return payload
}