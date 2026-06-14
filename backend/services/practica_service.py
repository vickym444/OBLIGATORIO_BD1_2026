from datetime import date, timedelta

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

    def listar_practicas_por_fecha(self, fecha):
        fecha = self._normalizar_fecha(fecha)
        return self.repository.get_practicas_by_fecha(fecha)

    def listar_practicas_por_rango_fechas(self, fecha_desde, fecha_hasta):
        fecha_desde = self._normalizar_fecha(fecha_desde)
        fecha_hasta = self._normalizar_fecha(fecha_hasta)
        if fecha_hasta < fecha_desde:
            raise ValueError("La fecha final no puede ser anterior a la fecha inicial")
        return self.repository.get_practicas_by_rango_fechas(fecha_desde, fecha_hasta)

    def _normalizar_fecha(self, fecha):
        if isinstance(fecha, date):
            return fecha
        return date.fromisoformat(str(fecha))

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

    def _nombre_dia_semana(self, fecha):
        dias = {
            0: "Lunes",
            1: "Martes",
            2: "Miercoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sabado",
            6: "Domingo",
        }
        return dias[fecha.weekday()]

    def generar_practicas_automaticas(self, id_actividad, fecha_desde=None, fecha_hasta=None):
        actividad = self._validar_actividad_activa(id_actividad)

        fecha_inicio = self._normalizar_fecha(fecha_desde) if fecha_desde else date.today()
        fecha_fin = self._normalizar_fecha(fecha_hasta) if fecha_hasta else fecha_inicio + timedelta(days=90)

        if fecha_fin < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la fecha inicial")

        dias_programados = self._dias_de_practica(actividad["dia"])
        generadas = []

        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            if self._nombre_dia_semana(fecha_actual) in dias_programados:
                practica_inactiva = self.repository.get_practica_by_actividad_y_fecha_inactiva(id_actividad, fecha_actual)
                if practica_inactiva:
                    self.repository.reactivate_practica(
                        practica_inactiva["id_practica"],
                        id_actividad,
                        fecha_actual,
                    )
                    generadas.append(practica_inactiva["id_practica"])
                else:
                    practica_activa = self.repository.get_practica_by_actividad_y_fecha(id_actividad, fecha_actual)
                    if not practica_activa:
                        generadas.append(
                            self.repository.create_practica(
                                id_actividad=id_actividad,
                                fecha=fecha_actual,
                            )
                        )
            fecha_actual += timedelta(days=1)

        return {
            "id_actividad": id_actividad,
            "desde": fecha_inicio,
            "hasta": fecha_fin,
            "generadas": len(generadas),
            "id_practicas": generadas,
        }

    def generar_practicas_futuras(self, id_actividad, dias_horizonte=7):
        return self.generar_practicas_automaticas(
            id_actividad=id_actividad,
            fecha_desde=date.today(),
            fecha_hasta=date.today() + timedelta(days=dias_horizonte),
        )

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