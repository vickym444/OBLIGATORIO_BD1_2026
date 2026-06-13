from repositories.asistencia_repository import AsistenciaRepository
from repositories.inscripcion_repository import InscripcionRepository


class AsistenciaService:
    def __init__(self, repository=None):
        self.repository = repository or AsistenciaRepository()
        self.inscripcion_repo = InscripcionRepository()

    def listar_asistencias(self):
        return self.repository.get_all_asistencias()

    def obtener_asistencia(self, id_asistencia):
        return self.repository.get_asistencia_by_id(id_asistencia)

    def obtener_por_inscripcion(self, id_inscripcion):
        return self.repository.get_asistencia_by_inscripcion(id_inscripcion)

    def registrar_asistencia(self, presente, id_inscripcion):
        # Verificar que la inscripcion existe y está activa
        inscripcion = self.inscripcion_repo.get_inscripcion_by_id(id_inscripcion)
        if not inscripcion:
            raise ValueError("La inscripción no existe")
        if inscripcion["fecha_baja"] is not None:
            raise ValueError("La inscripción está dada de baja")
        if inscripcion["estado"] == "cancelada":
            raise ValueError("La inscripción está cancelada")

        # Verificar que no existe ya una asistencia para esta inscripcion
        existente = self.repository.get_asistencia_by_inscripcion(id_inscripcion)
        if existente:
            raise ValueError("Ya existe una asistencia registrada para esta inscripción")

        return self.repository.create_asistencia(
            presente=presente,
            id_inscripcion=id_inscripcion
        )

    def actualizar_asistencia(self, id_asistencia, presente):
        asistencia = self.repository.get_asistencia_by_id(id_asistencia)
        if not asistencia:
            raise ValueError("La asistencia no existe")
        return self.repository.update_asistencia(id_asistencia, presente)


asistencia_service = AsistenciaService()