class Facultad:
    def __init__(self, id_facultad, nombre):
        self.id_facultad = id_facultad
        self.nombre = nombre


class Carrera:
    def __init__(self, id_carrera, nombre, id_facultad):
        self.id_carrera = id_carrera
        self.nombre = nombre
        self.id_facultad = id_facultad

class Estudiante:
    def __init__(self, id_estudiante, documento, nombre, apellido, email, id_carrera, activo):
        self.id_estudiante = id_estudiante
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.id_carrera = id_carrera
        self.activo = activo

class Asistencia:
    def __init__(self, id_asistencia, id_inscripcion, presente):
        self.id_asistencia = id_asistencia
        self.id_inscripcion = id_inscripcion
        self.presente = presente

class Inscripcion:
    def __init__(self, id_estudiante, id_inscripcion, fecha_inscripcion, fecha_baja, id_practica, estado):
        self.id_estudiante = id_estudiante
        self.id_inscripcion = id_inscripcion
        self.fecha_inscripcion = fecha_inscripcion
        self.fecha_baja = fecha_baja
        self.id_practica = id_practica
        self.estado = estado

class Practica:
    def __init__(self, id_actividad, id_practica, fecha):
        self.id_actividad = id_actividad
        self.id_practica = id_practica
        self.fecha = fecha

class Espacio:
    def __init__(self, descripcion, id_espacio, nombre):
        self.descripcion = descripcion
        self.id_espacio = id_espacio
        self.nombre = nombre

class Disciplina:
    def __init__(self, descripcion, id_disciplina, nombre):
        self.descripcion = descripcion
        self.id_disciplina = id_disciplina
        self.nombre = nombre

class Actividad:
    def __init__(self, id_actividad, nombre, id_disciplina, id_espacio, cupo_maximo, cupo_minimo, dia, hora_inicio, hora_fin, estado):
        self.id_actividad = id_actividad
        self.nombre = nombre
        self.id_disciplina = id_disciplina
        self.id_espacio = id_espacio
        self.cupo_maximo = cupo_maximo
        self.cupo_minimo = cupo_minimo
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
