from repositories.inscripcion_repository import InscripcionRepository
from repositories.practica_repository import PracticaRepository
from repositories.actividad_repository import ActividadRepository
from datetime import date


class InscripcionService:
    def __init__(self, repository=None):
        self.repository = repository or InscripcionRepository()
        self.practica_repo = PracticaRepository()
        self.actividad_repo = ActividadRepository()

    def listar_inscripciones(
        self,
        fecha_desde=None,
        fecha_hasta=None,
        id_facultad=None,
        id_carrera=None,
        id_actividad=None,
        id_disciplina=None,
    ):
        return self.repository.get_all_inscripciones(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            id_facultad=id_facultad,
            id_carrera=id_carrera,
            id_actividad=id_actividad,
            id_disciplina=id_disciplina,
        )

    def obtener_inscripcion(self, id_inscripcion):
        return self.repository.get_inscripcion_by_id(id_inscripcion)

    def listar_por_estudiante(self, id_estudiante):
        return self.repository.get_inscripciones_by_estudiante(id_estudiante)

    def listar_por_practica(self, id_practica):
        return self.repository.get_inscripciones_by_practica(id_practica)

    def listar_mias(self, id_estudiante):
        return self.repository.get_inscripciones_activas_by_estudiante(id_estudiante)

    def _dias_de_actividad(self, dia):
        mapa = {
            'Lunes': {'Lunes'},
            'Martes': {'Martes'},
            'Miercoles': {'Miercoles'},
            'Jueves': {'Jueves'},
            'Viernes': {'Viernes'},
            'Lunes y Miercoles': {'Lunes', 'Miercoles'},
            'Martes y Jueves': {'Martes', 'Jueves'},
            'Miercoles y Viernes': {'Miercoles', 'Viernes'},
        }
        return mapa.get(dia, {dia})

    def _se_superponen_horarios(self, actividad_a, actividad_b):
        dias_a = self._dias_de_actividad(actividad_a['dia'])
        dias_b = self._dias_de_actividad(actividad_b['dia'])

        if not dias_a.intersection(dias_b):
            return False

        inicio_a = str(actividad_a['hora_inicio'])
        fin_a = str(actividad_a['hora_fin'])
        inicio_b = str(actividad_b['hora_inicio'])
        fin_b = str(actividad_b['hora_fin'])

        return inicio_a < fin_b and inicio_b < fin_a

    def _validar_practica_abierta(self, practica, actividad):
        if not practica or practica.get('activo') != 1:
            raise ValueError('La práctica no existe o está inactiva')
        if not actividad or actividad.get('activo') != 1:
            raise ValueError('La actividad no existe o está inactiva')
        if actividad.get('estado') != 'abierta':
            raise ValueError('La práctica no admite inscripciones en este momento')

    def _validar_sin_duplicado(self, id_estudiante, id_practica):
        existente = self.repository.get_inscripcion_activa(id_estudiante, id_practica)
        if existente:
            raise ValueError('Ya estás inscripto a esta práctica')

    def _validar_sin_choque_horario(self, id_estudiante, id_practica_objetivo, actividad_objetivo):
        inscripciones_activas = self.repository.get_inscripciones_activas_by_estudiante(id_estudiante)
        for inscripcion in inscripciones_activas:
            if inscripcion['id_practica'] == id_practica_objetivo:
                continue
            if self._se_superponen_horarios(inscripcion, actividad_objetivo):
                raise ValueError('Ya tenés otra práctica inscripta en ese mismo horario')

    def crear_inscripcion(self, fecha_inscripcion, estado, id_estudiante, id_practica):
        practica = self.practica_repo.get_practica_by_id(id_practica)
        actividad = None
        if practica:
            actividad = self.actividad_repo.get_actividad_by_id(practica['id_actividad'])

        self._validar_practica_abierta(practica, actividad)
        self._validar_sin_duplicado(id_estudiante, id_practica)
        self._validar_sin_choque_horario(id_estudiante, id_practica, actividad)

        total_confirmadas = self.repository.count_inscripciones_activas(id_practica)
        estado_final = 'confirmada' if total_confirmadas < int(actividad['cupo_maximo']) else 'en_espera'

        return self.repository.create_inscripcion(
            fecha_inscripcion=fecha_inscripcion,
            estado=estado_final,
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

        filas = self.repository.dar_baja(id_inscripcion, fecha_baja)
        if not filas:
            return filas

        if inscripcion["estado"] == "confirmada":
            siguiente_espera = self.repository.get_inscripcion_en_espera_anterior(inscripcion["id_practica"])
            if siguiente_espera:
                self.repository.update_estado(siguiente_espera["id_inscripcion"], "confirmada")

        return filas


inscripcion_service = InscripcionService()