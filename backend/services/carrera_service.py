from repositories.carrera_repository import CarreraRepository


class CarreraService:
    def __init__(self, repository=None):
        self.repository = repository or CarreraRepository()

    def listar_carreras(self):
        return self.repository.get_all_carreras()

    def obtener_carrera(self, id_carrera):
        return self.repository.get_carrera_by_id(id_carrera)

    def crear_carrera(self, nombre, id_facultad):
        return self.repository.create_carrera(nombre=nombre, id_facultad=id_facultad)

    def actualizar_carrera(self, id_carrera, nombre, id_facultad, activo):
        return self.repository.update_carrera(
            id_carrera=id_carrera,
            nombre=nombre,
            id_facultad=id_facultad,
            activo=activo,
        )

    def eliminar_carrera(self, id_carrera):
        return self.repository.delete_carrera(id_carrera)


carrera_service = CarreraService()