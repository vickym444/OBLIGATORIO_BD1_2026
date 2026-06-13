from repositories.estudiante_repository import EstudianteRepository

repo = EstudianteRepository()

def listar_estudiantes():
    return repo.get_all_estudiantes()

def obtener_estudiante(id_estudiante: int):
    return repo.get_estudiante_by_id(id_estudiante)

def crear_estudiante(documento, nombre, apellido, email, id_carrera):
    return repo.create_estudiante(documento, nombre, apellido, email, id_carrera)

def actualizar_estudiante(id_estudiante, documento, nombre, apellido, email, activo, id_carrera):
    return repo.update_estudiante(id_estudiante, documento, nombre, apellido, email, activo, id_carrera)

def eliminar_estudiante(id_estudiante: int):
    return repo.delete_estudiante(id_estudiante)