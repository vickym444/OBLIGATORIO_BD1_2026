import { request } from './apiClient'

export function listarPracticas() {
  return request('/practicas')
}

export function listarPracticasPorActividad(idActividad) {
  return request(`/practicas/actividad/${idActividad}`)
}

export function listarPracticasPorFecha(fecha, ordenarPorcentaje = false, soloCuposDisponibles = false) {
  const params = new URLSearchParams()

  if (ordenarPorcentaje) {
    params.set('ordenar_porcentaje', 'true')
  }

  if (soloCuposDisponibles) {
    params.set('solo_cupos_disponibles', 'true')
  }

  const query = params.toString()
  return request(`/practicas/fecha/${fecha}${query ? `?${query}` : ''}`)
}

export function listarPracticasPorRango(fechaDesde, fechaHasta, ordenarPorcentaje = false, soloCuposDisponibles = false) {
  const params = new URLSearchParams({
    fecha_desde: fechaDesde,
    fecha_hasta: fechaHasta,
  })

  if (ordenarPorcentaje) {
    params.set('ordenar_porcentaje', 'true')
  }

  if (soloCuposDisponibles) {
    params.set('solo_cupos_disponibles', 'true')
  }

  return request(`/practicas/rango?${params.toString()}`)
}

export function generarPracticas(idActividad, fechaDesde, fechaHasta) {
  const params = new URLSearchParams()

  if (fechaDesde) {
    params.set('fecha_desde', fechaDesde)
  }

  if (fechaHasta) {
    params.set('fecha_hasta', fechaHasta)
  }

  const queryString = params.toString()
  return request(`/practicas/generar/${idActividad}${queryString ? `?${queryString}` : ''}`, {
    method: 'POST',
  })
}