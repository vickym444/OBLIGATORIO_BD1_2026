from repositories.estudiante_repository import EstudianteRepository


class EstudianteService:
    def __init__(self, repository=None):
        self.repository = repository or EstudianteRepository()

    def listar_estudiantes(self):
        return self.repository.get_all_estudiantes()

    def obtener_estudiante(self, id_estudiante):
        return self.repository.get_estudiante_by_id(id_estudiante)

    def crear_estudiante(self, documento, nombre, apellido, email, id_carrera, activo=1):
        return self.repository.create_estudiante(
            documento=documento,
            nombre=nombre,
            apellido=apellido,
            email=email,
            id_carrera=id_carrera,
            activo=activo,
        )

    def actualizar_estudiante(self, id_estudiante, documento, nombre, apellido, email, activo, id_carrera):
        return self.repository.update_estudiante(
            id_estudiante=id_estudiante,
            documento=documento,
            nombre=nombre,
            apellido=apellido,
            email=email,
            activo=activo,
            id_carrera=id_carrera,
        )

    def eliminar_estudiante(self, id_estudiante):
        return self.repository.delete_estudiante(id_estudiante)


estudiante_service = EstudianteService()