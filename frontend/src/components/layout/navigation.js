export const navigationItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Facultades', path: '/facultades' },
  { label: 'Carreras', path: '/carreras' },
  { label: 'Estudiantes', path: '/estudiantes' },
  { label: 'Disciplinas', path: '/disciplinas' },
  { label: 'Espacios', path: '/espacios' },
  { label: 'Actividades', path: '/actividades' },
  { label: 'Inscripciones', path: '/inscripciones' },
  { label: 'Asistencias', path: '/asistencias' },
  { label: 'Reportes', path: '/reportes' },
  { label: 'Usuarios', path: '/usuarios' },
]

export const sectionLabels = navigationItems.reduce(
  (labels, item) => {
    labels[item.path] = item.label
    return labels
  },
  { '/': 'Dashboard' },
)