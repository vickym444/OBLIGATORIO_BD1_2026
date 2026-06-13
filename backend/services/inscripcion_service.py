from repositories.inscripcion_repository import InscripcionRepository
from repositories.practica_repository import PracticaRepository
from repositories.actividad_repository import ActividadRepository


class InscripcionService:
    def __init__(self, repository=None):
        self.repository = repository or InscripcionRepository()
        self.practica_repo = PracticaRepository()
        self.actividad_repo = ActividadRepository()

    def listar_inscripciones(self):
        return self.repository.get_all_inscripciones()

    def obtener_inscripcion(self, id_inscripcion):
        return self.repository.get_inscripcion_by_id(id_inscripcion)

    def listar_por_estudiante(self, id_estudiante):
        return self.repository.get_inscripciones_by_estudiante(id_estudiante)

    def listar_por_practica(self, id_practica):
        return self.repository.get_inscripciones_by_practica(id_practica)

    def crear_inscripcion(self, fecha_inscripcion, estado, id_estudiante, id_practica):
        # Verificar que la practica existe
        practica = self.practica_repo.get_practica_by_id(id_practica)
        if not practica:
            raise ValueError("La práctica no existe")

        # Verificar que la actividad está abierta
        actividad = self.actividad_repo.get_actividad_by_id(practica["id_actividad"])
        if not actividad:
            raise ValueError("La actividad no existe")
        if actividad["estado"] != "abierta":
            raise ValueError(f"La actividad no está abierta, estado actual: {actividad['estado']}")

        # Verificar que no existe inscripcion activa duplicada
        existente = self.repository.get_inscripcion_activa(id_estudiante, id_practica)
        if existente:
            raise ValueError("El estudiante ya tiene una inscripción activa en esta práctica")

        # Verificar cupo disponible
        total_inscriptos = self.repository.count_inscripciones_activas(id_practica)
        if total_inscriptos >= actividad["cupo_maximo"]:
            raise ValueError("La actividad no tiene cupo disponible")

        return self.repository.create_inscripcion(
            fecha_inscripcion=fecha_inscripcion,
            estado=estado,
            id_estudiante=id_estudiante,
            id_practica=id_practica
        )

    def actualizar_estado(self, id_inscripcion, estado):
        inscripcion = self.repository.get_inscripcion_by_id(id_inscripcion)
        if not inscripcion:
            raise ValueError("La inscripción no existe")
        return self.repository.update_estado(id_inscripcion, estado)

    def dar_baja(self, id_inscripcion, fecha_baja):
        inscripcion = self.repository.get_inscripcion_by_id(id_inscripcion)
        if not inscripcion:
            raise ValueError("La inscripción no existe")
        if inscripcion["fecha_baja"] is not None:
            raise ValueError("La inscripción ya fue dada de baja")
        return self.repository.dar_baja(id_inscripcion, fecha_baja)


inscripcion_service = InscripcionService()