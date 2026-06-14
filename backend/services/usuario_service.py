from repositories.usuario_repository import UsuarioRepository
from repositories.estudiante_repository import EstudianteRepository
from core.auth_security import get_password_hash


class UsuarioService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()
        self.estudiante_repository = EstudianteRepository()

    def _hashear_password(self, password):
        return get_password_hash(password)

    def _validar_rol_estudiante(self, rol, id_estudiante):
        if rol == 'admin' and id_estudiante is not None:
            raise ValueError("Un usuario admin no puede tener id_estudiante")
        if rol == 'estudiante' and id_estudiante is None:
            raise ValueError("Un usuario estudiante debe tener id_estudiante")

    def _validar_estudiante_activo(self, id_estudiante):
        estudiante = self.estudiante_repository.get_estudiante_by_id(id_estudiante)
        if not estudiante or estudiante.get("activo") != 1:
            raise ValueError("El estudiante no existe o está inactivo")

    def _validar_email_disponible(self, email, id_usuario_excluir=None):
        usuario = self.repository.get_usuario_by_email(email)
        if usuario and usuario["id_usuario"] != id_usuario_excluir:
            raise ValueError("Ya existe un usuario con ese email")

    def listar_usuarios(self):
        return self.repository.get_all_usuarios()

    def obtener_usuario(self, id_usuario):
        return self.repository.get_usuario_by_id(id_usuario)

    def crear_usuario(self, email, password, rol, id_estudiante):
        email = str(email).strip()

        if not email:
            raise ValueError("El email es obligatorio")
        if not password:
            raise ValueError("La contraseña es obligatoria")

        self._validar_rol_estudiante(rol, id_estudiante)

        if id_estudiante is not None:
            self._validar_estudiante_activo(id_estudiante)

        self._validar_email_disponible(email)

        password_hash = self._hashear_password(password)

        return self.repository.create_usuario(
            email=email,
            password_hash=password_hash,
            rol=rol,
            id_estudiante=id_estudiante
        )

    def actualizar_usuario(self, id_usuario, email, password, rol, id_estudiante, activo):
        email = str(email).strip()

        if not email:
            raise ValueError("El email es obligatorio")
        if not password:
            raise ValueError("La contraseña es obligatoria")

        self._validar_rol_estudiante(rol, id_estudiante)

        if id_estudiante is not None:
            self._validar_estudiante_activo(id_estudiante)

        self._validar_email_disponible(email, id_usuario_excluir=id_usuario)

        password_hash = self._hashear_password(password)

        return self.repository.update_usuario(
            id_usuario=id_usuario,
            email=email,
            password_hash=password_hash,
            rol=rol,
            id_estudiante=id_estudiante,
            activo=activo
        )

    def eliminar_usuario(self, id_usuario):
        return self.repository.delete_usuario(id_usuario)


usuario_service = UsuarioService()