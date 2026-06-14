from repositories.actividad_repository import ActividadRepository
from datetime import time, timedelta


class ActividadService:
    def __init__(self, repository=None):
        self.repository = repository or ActividadRepository()

    def listar_actividades(self):
        return self.repository.get_all_actividades()

    def obtener_actividad(self, id_actividad):
        return self.repository.get_actividad_by_id(id_actividad)

    def _dias_de_practica(self, dia):
        dia_valor = getattr(dia, "value", dia)
        dias_map = {
            "Lunes": {"Lunes"},
            "Martes": {"Martes"},
            "Miercoles": {"Miercoles"},
            "Jueves": {"Jueves"},
            "Viernes": {"Viernes"},
            "Lunes y Miercoles": {"Lunes", "Miercoles"},
            "Martes y Jueves": {"Martes", "Jueves"},
            "Miercoles y Viernes": {"Miercoles", "Viernes"},
        }
        return dias_map.get(dia_valor, {str(dia_valor)})

    def _normalizar_hora(self, hora):
        if isinstance(hora, time):
            return hora
        if isinstance(hora, timedelta):
            total_seconds = int(hora.total_seconds())
            horas, resto = divmod(total_seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            return time(hour=horas, minute=minutos, second=segundos)
        if hasattr(hora, "hour") and hasattr(hora, "minute") and hasattr(hora, "second"):
            return time(hour=hora.hour, minute=hora.minute, second=hora.second)
        return time.fromisoformat(str(hora))

    def _hay_superposicion(self, nueva_hora_inicio, nueva_hora_fin, hora_inicio_existente, hora_fin_existente):
        return nueva_hora_inicio < hora_fin_existente and nueva_hora_fin > hora_inicio_existente

    def _validar_conflicto_horario(self, id_actividad, hora_inicio, hora_fin, dia, id_espacio):
        actividades_en_espacio = self.repository.get_actividades_activas_por_espacio(
            id_espacio,
            id_actividad_excluir=id_actividad,
        )

        dias_nuevos = self._dias_de_practica(dia)
        hora_inicio_nueva = self._normalizar_hora(hora_inicio)
        hora_fin_nueva = self._normalizar_hora(hora_fin)

        for actividad in actividades_en_espacio:
            dias_existentes = self._dias_de_practica(actividad["dia"])
            if not dias_nuevos.intersection(dias_existentes):
                continue

            hora_inicio_existente = self._normalizar_hora(actividad["hora_inicio"])
            hora_fin_existente = self._normalizar_hora(actividad["hora_fin"])

            if self._hay_superposicion(
                hora_inicio_nueva,
                hora_fin_nueva,
                hora_inicio_existente,
                hora_fin_existente,
            ):
                raise ValueError(
                    f"La actividad se superpone con '{actividad['nombre']}' en el mismo espacio y horario"
                )

    def crear_actividad(self, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la actividad es obligatorio")

        if cupo_minimo > cupo_maximo:
            raise ValueError("El cupo mínimo no puede ser mayor al cupo máximo")

        self._validar_conflicto_horario(
            id_actividad=None,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            dia=dia,
            id_espacio=id_espacio,
        )

        actividad_inactiva = self.repository.get_actividad_by_nombre_inactiva(nombre)
        if actividad_inactiva:
            self.repository.reactivate_actividad(actividad_inactiva["id_actividad"])
            return actividad_inactiva["id_actividad"]

        return self.repository.create_actividad(
            nombre=nombre,
            cupo_maximo=cupo_maximo,
            cupo_minimo=cupo_minimo,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            dia=dia,
            estado=estado,
            id_disciplina=id_disciplina,
            id_espacio=id_espacio
        )

    def actualizar_actividad(self, id_actividad, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio, activo):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la actividad es obligatorio")

        if cupo_minimo > cupo_maximo:
            raise ValueError("El cupo mínimo no puede ser mayor al cupo máximo")

        self._validar_conflicto_horario(
            id_actividad=id_actividad,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            dia=dia,
            id_espacio=id_espacio,
        )

        return self.repository.update_actividad(
            id_actividad=id_actividad,
            nombre=nombre,
            cupo_maximo=cupo_maximo,
            cupo_minimo=cupo_minimo,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            dia=dia,
            estado=estado,
            id_disciplina=id_disciplina,
            id_espacio=id_espacio,
            activo=activo
        )

    def eliminar_actividad(self, id_actividad):
        return self.repository.delete_actividad(id_actividad)


actividad_service = ActividadService()