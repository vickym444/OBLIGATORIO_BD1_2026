from repositories.asistencia_repository import AsistenciaRepository
from repositories.inscripcion_repository import InscripcionRepository
from repositories.practica_repository import PracticaRepository


class AsistenciaService:
    def __init__(self, repository=None):
        self.repository = repository or AsistenciaRepository()
        self.inscripcion_repo = InscripcionRepository()
        self.practica_repo = PracticaRepository()

    def listar_asistencias(self):
        return self.repository.get_all_asistencias()

    def listar_practicas_para_asistencia(self, fecha_desde, fecha_hasta):
        practicas = self.practica_repo.get_practicas_by_rango_fechas(fecha_desde, fecha_hasta)
        resultado = []

        for practica in practicas:
            inscriptos = self.inscripcion_repo.get_inscripciones_confirmadas_con_asistencia_by_practica(
                practica["id_practica"]
            )
            practica_con_inscriptos = dict(practica)
            practica_con_inscriptos["inscriptos"] = inscriptos
            practica_con_inscriptos["total_inscriptos"] = len(inscriptos)
            practica_con_inscriptos["total_presentes"] = sum(
                1 for inscripcion in inscriptos if bool(inscripcion.get("presente"))
            )
            resultado.append(practica_con_inscriptos)

        return resultado

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

    def guardar_asistencias_lote(self, registros):
        if not registros:
            raise ValueError("No se enviaron asistencias para guardar")

        filas_upsert = []
        for registro in registros:
            inscripcion = self.inscripcion_repo.get_inscripcion_by_id(registro.id_inscripcion)
            if not inscripcion:
                raise ValueError(f"La inscripción {registro.id_inscripcion} no existe")
            if inscripcion["fecha_baja"] is not None:
                raise ValueError(f"La inscripción {registro.id_inscripcion} está dada de baja")
            if inscripcion["estado"] != "confirmada":
                raise ValueError(
                    f"La inscripción {registro.id_inscripcion} no está confirmada"
                )

            filas_upsert.append((1 if registro.presente else 0, registro.id_inscripcion))

        return self.repository.upsert_asistencias(filas_upsert)


asistencia_service = AsistenciaService()