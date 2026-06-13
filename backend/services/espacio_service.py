from repositories.espacio_repository import EspacioRepository


class EspacioService:
    def __init__(self, repository=None):
        self.repository = repository or EspacioRepository()

    def listar_espacios(self):
        return self.repository.get_all_espacios()

    def obtener_espacio(self, id_espacio):
        return self.repository.get_espacio_by_id(id_espacio)

    def crear_espacio(self, nombre, descripcion=None):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del espacio es obligatorio")

        espacio_inactivo = self.repository.get_espacio_by_nombre_inactivo(nombre)
        if espacio_inactivo:
            self.repository.reactivate_espacio(espacio_inactivo["id_espacio"])
            return espacio_inactivo["id_espacio"]

        espacio_activo = self.repository.get_espacio_by_nombre_activo(nombre)
        if espacio_activo:
            raise ValueError("Ya existe un espacio activo con ese nombre")

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