from repositories.actividad_repository import ActividadRepository


class ActividadService:
    def __init__(self, repository=None):
        self.repository = repository or ActividadRepository()

    def listar_actividades(self):
        return self.repository.get_all_actividades()

    def obtener_actividad(self, id_actividad):
        return self.repository.get_actividad_by_id(id_actividad)

    def crear_actividad(self, nombre, cupo_maximo, cupo_minimo, hora_inicio, hora_fin, dia, estado, id_disciplina, id_espacio):
        if cupo_minimo > cupo_maximo:
            raise ValueError("El cupo mínimo no puede ser mayor al cupo máximo")
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
        if cupo_minimo > cupo_maximo:
            raise ValueError("El cupo mínimo no puede ser mayor al cupo máximo")
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