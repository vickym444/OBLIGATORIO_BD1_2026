from repositories.facultad_repository import FacultadRepository

repo = FacultadRepository()

def listar_facultades():
    return repo.get_all_facultades()

def obtener_facultad(id_facultad: int):
    return repo.get_facultad_by_id(id_facultad)

def crear_facultad(nombre):
    return repo.create_facultad(nombre)

def actualizar_facultad(id_facultad, nombre, activo):
    return repo.update_facultad(id_facultad, nombre, activo)

def eliminar_facultad(id_facultad: int):
    return repo.delete_facultad(id_facultad)