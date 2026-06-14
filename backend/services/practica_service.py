from datetime import date

from repositories.actividad_repository import ActividadRepository
from repositories.practica_repository import PracticaRepository


class PracticaService:
    def __init__(self, repository=None):
        self.repository = repository or PracticaRepository()
        self.actividad_repository = ActividadRepository()

    def listar_practicas(self):
        return self.repository.get_all_practicas()

    def listar_practicas_por_actividad(self, id_actividad):
        return self.repository.get_practicas_by_actividad(id_actividad)

    def obtener_practica(self, id_practica):
        return self.repository.get_practica_by_id(id_practica)

    def _normalizar_fecha(self, fecha):
        if isinstance(fecha, date):
            return fecha
        return date.fromisoformat(str(fecha))

    def _validar_actividad_activa(self, id_actividad):
        actividad = self.actividad_repository.get_actividad_by_id(id_actividad)
        if not actividad:
            raise ValueError("La actividad no existe")
        if actividad["activo"] != 1:
            raise ValueError("La actividad seleccionada está inactiva")
        return actividad

    def _validar_practica_disponible(self, id_actividad, fecha):
        practica = self.repository.get_practica_by_actividad_y_fecha(id_actividad, fecha)
        if practica and practica["activo"] == 1:
            raise ValueError("Ya existe una práctica activa para esa actividad y fecha")
        return practica

    def crear_practica(self, id_actividad, fecha):
        fecha = self._normalizar_fecha(fecha)
        self._validar_actividad_activa(id_actividad)

        practica_inactiva = self.repository.get_practica_by_actividad_y_fecha_inactiva(id_actividad, fecha)
        if practica_inactiva:
            self.repository.reactivate_practica(practica_inactiva["id_practica"], id_actividad, fecha)
            return practica_inactiva["id_practica"]

        self._validar_practica_disponible(id_actividad, fecha)

        return self.repository.create_practica(
            id_actividad=id_actividad,
            fecha=fecha
        )

    def actualizar_practica(self, id_practica, id_actividad, fecha, activo):
        fecha = self._normalizar_fecha(fecha)
        self._validar_actividad_activa(id_actividad)

        practica_existente = self.repository.get_practica_by_actividad_y_fecha(id_actividad, fecha)
        if practica_existente and practica_existente["id_practica"] != id_practica and practica_existente["activo"] == 1:
            raise ValueError("Ya existe una práctica activa para esa actividad y fecha")

        return self.repository.update_practica(
            id_practica=id_practica,
            id_actividad=id_actividad,
            fecha=fecha,
            activo=activo
        )

    def eliminar_practica(self, id_practica):
        return self.repository.delete_practica(id_practica)


practica_service = PracticaService()