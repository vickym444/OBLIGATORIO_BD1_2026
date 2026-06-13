from repositories.practica_repository import PracticaRepository


class PracticaService:
    def __init__(self, repository=None):
        self.repository = repository or PracticaRepository()

    def listar_practicas(self):
        return self.repository.get_all_practicas()

    def listar_practicas_por_actividad(self, id_actividad):
        return self.repository.get_practicas_by_actividad(id_actividad)

    def obtener_practica(self, id_practica):
        return self.repository.get_practica_by_id(id_practica)

    def crear_practica(self, id_actividad, fecha):
        return self.repository.create_practica(
            id_actividad=id_actividad,
            fecha=fecha
        )

    def actualizar_practica(self, id_practica, id_actividad, fecha, activo):
        return self.repository.update_practica(
            id_practica=id_practica,
            id_actividad=id_actividad,
            fecha=fecha,
            activo=activo
        )

    def eliminar_practica(self, id_practica):
        return self.repository.delete_practica(id_practica)


practica_service = PracticaService()