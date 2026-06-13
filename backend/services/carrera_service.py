from repositories.carrera_repository import CarreraRepository

repo = CarreraRepository()

def listar_carreras():
    return repo.get_all_carreras()

def obtener_carrera(id_carrera: int):
    return repo.get_carrera_by_id(id_carrera)

def crear_carrera(nombre, id_facultad):
    return repo.create_carrera(nombre, id_facultad)

def actualizar_carrera(id_carrera, nombre, id_facultad, activo):
    return repo.update_carrera(id_carrera, nombre, id_facultad, activo)

def eliminar_carrera(id_carrera: int):
    return repo.delete_carrera(id_carrera)