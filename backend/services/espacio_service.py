from repositories.espacio_repository import EspacioRepository

repo = EspacioRepository()

def listar_espacios():
    return repo.get_all_espacios()

def obtener_espacio(id_espacio: int):
    return repo.get_espacio_by_id(id_espacio)

def crear_espacio(nombre, descripcion):
    return repo.create_espacio(nombre, descripcion)

def actualizar_espacio(id_espacio, nombre, descripcion, activo):
    return repo.update_espacio(id_espacio, nombre, descripcion, activo)

def eliminar_espacio(id_espacio: int):
    return repo.delete_espacio(id_espacio)