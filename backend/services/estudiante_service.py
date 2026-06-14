from repositories.estudiante_repository import EstudianteRepository
from repositories.carrera_repository import CarreraRepository


class EstudianteService:
    def __init__(self, repository=None):
        self.repository = repository or EstudianteRepository()
        self.carrera_repository = CarreraRepository()

    def listar_estudiantes(self):
        return self.repository.get_all_estudiantes()

    def obtener_estudiante(self, id_estudiante):
        return self.repository.get_estudiante_by_id(id_estudiante)

    def _normalizar_texto(self, valor):
        return str(valor).strip()

    def _normalizar_email(self, valor):
        return str(valor).strip().lower()

    def _validar_carrera_activa(self, id_carrera):
        carrera = self.carrera_repository.get_carrera_by_id(id_carrera)
        if not carrera or carrera.get("activo") != 1:
            raise ValueError("La carrera seleccionada no existe o está inactiva")

    def _validar_documento_disponible(self, documento, id_estudiante_excluir=None):
        estudiante = self.repository.get_estudiante_by_documento(documento)
        if estudiante and estudiante["id_estudiante"] != id_estudiante_excluir:
            raise ValueError("Ya existe un estudiante con ese documento")

    def _validar_email_disponible(self, email, id_estudiante_excluir=None):
        estudiante = self.repository.get_estudiante_by_email(email)
        if estudiante and estudiante["id_estudiante"] != id_estudiante_excluir:
            raise ValueError("Ya existe un estudiante con ese email")

    def crear_estudiante(self, documento, nombre, apellido, email, id_carrera, activo=1):
        documento = self._normalizar_texto(documento)
        nombre = self._normalizar_texto(nombre)
        apellido = self._normalizar_texto(apellido)
        email = self._normalizar_email(email)

        if not documento:
            raise ValueError("El documento del estudiante es obligatorio")
        if not nombre:
            raise ValueError("El nombre del estudiante es obligatorio")
        if not apellido:
            raise ValueError("El apellido del estudiante es obligatorio")
        if not email:
            raise ValueError("El email del estudiante es obligatorio")

        self._validar_carrera_activa(id_carrera)

        estudiante_existente = self.repository.get_estudiante_by_documento(documento)
        if estudiante_existente:
            if estudiante_existente["activo"] == 1:
                raise ValueError("Ya existe un estudiante activo con ese documento")

            self._validar_email_disponible(email, estudiante_existente["id_estudiante"])
            self.repository.update_estudiante(
                id_estudiante=estudiante_existente["id_estudiante"],
                documento=documento,
                nombre=nombre,
                apellido=apellido,
                email=email,
                activo=1,
                id_carrera=id_carrera,
            )
            return estudiante_existente["id_estudiante"]

        self._validar_documento_disponible(documento)
        self._validar_email_disponible(email)

        return self.repository.create_estudiante(
            documento=documento,
            nombre=nombre,
            apellido=apellido,
            email=email,
            id_carrera=id_carrera,
            activo=activo,
        )

    def actualizar_estudiante(self, id_estudiante, documento, nombre, apellido, email, activo, id_carrera):
        documento = self._normalizar_texto(documento)
        nombre = self._normalizar_texto(nombre)
        apellido = self._normalizar_texto(apellido)
        email = self._normalizar_email(email)

        if not documento:
            raise ValueError("El documento del estudiante es obligatorio")
        if not nombre:
            raise ValueError("El nombre del estudiante es obligatorio")
        if not apellido:
            raise ValueError("El apellido del estudiante es obligatorio")
        if not email:
            raise ValueError("El email del estudiante es obligatorio")

        self._validar_carrera_activa(id_carrera)

        estudiante_existente = self.repository.get_estudiante_by_documento(documento)
        if estudiante_existente and estudiante_existente["id_estudiante"] != id_estudiante:
            raise ValueError("Ya existe un estudiante con ese documento")

        estudiante_email = self.repository.get_estudiante_by_email(email)
        if estudiante_email and estudiante_email["id_estudiante"] != id_estudiante:
            raise ValueError("Ya existe un estudiante con ese email")

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