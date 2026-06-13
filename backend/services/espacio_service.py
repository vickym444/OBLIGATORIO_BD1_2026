from repositories.espacio_repository import EspacioRepository


class EspacioService:
    def __init__(self, repository=None):
        self.repository = repository or EspacioRepository()

    def listar_espacios(self):
        return self.repository.get_all_espacios()

    def obtener_espacio(self, id_espacio):
        return self.repository.get_espacio_by_id(id_espacio)

    def crear_espacio(self, nombre, descripcion=None):
        return self.repository.create_espacio(nombre=nombre, descripcion=descripcion)

    def actualizar_espacio(self, id_espacio, nombre, descripcion, activo):
        return self.repository.update_espacio(
            id_espacio=id_espacio,
            nombre=nombre,
            descripcion=descripcion,
            activo=activo,
        )

    def eliminar_espacio(self, id_espacio):
        return self.repository.delete_espacio(id_espacio)


espacio_service = EspacioService()