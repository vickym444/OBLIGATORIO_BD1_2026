import { request } from './apiClient'

export function listarPracticasParaAsistencia(fechaDesde, fechaHasta) {
  const params = new URLSearchParams()

  if (fechaDesde) {
    params.set('fecha_desde', fechaDesde)
  }

  if (fechaHasta) {
    params.set('fecha_hasta', fechaHasta)
  }

  const query = params.toString()
  return request(`/asistencias/rango${query ? `?${query}` : ''}`)
}

export function guardarAsistenciasLote(registros) {
  return request('/asistencias/lote', {
    method: 'POST',
    body: JSON.stringify({ registros }),
  })
}
