from repositories.usuario_repository import UsuarioRepository
from repositories.estudiante_repository import EstudianteRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()
        self.estudiante_repository = EstudianteRepository()

    def _hashear_password(self, password):
        return pwd_context.hash(password)

    def _validar_rol_estudiante(self, rol, id_estudiante):
        if rol == 'admin' and id_estudiante is not None:
            raise ValueError("Un usuario admin no puede tener id_estudiante")
        if rol == 'estudiante' and id_estudiante is None:
            raise ValueError("Un usuario estudiante debe tener id_estudiante")

    def _validar_estudiante_activo(self, id_estudiante):
        estudiante = self.estudiante_repository.get_estudiante_by_id(id_estudiante)
        if not estudiante or estudiante.get("activo") != 1:
            raise ValueError("El estudiante no existe o está inactivo")

    def _validar_username_disponible(self, username, id_usuario_excluir=None):
        usuario = self.repository.get_usuario_by_username(username)
        if usuario and usuario["id_usuario"] != id_usuario_excluir:
            raise ValueError("Ya existe un usuario con ese username")

    def listar_usuarios(self):
        return self.repository.get_all_usuarios()

    def obtener_usuario(self, id_usuario):
        return self.repository.get_usuario_by_id(id_usuario)

    def crear_usuario(self, username, password, rol, id_estudiante):
        username = str(username).strip()

        if not username:
            raise ValueError("El username es obligatorio")
        if not password:
            raise ValueError("La contraseña es obligatoria")

        self._validar_rol_estudiante(rol, id_estudiante)

        if id_estudiante is not None:
            self._validar_estudiante_activo(id_estudiante)

        self._validar_username_disponible(username)

        password_hash = self._hashear_password(password)

        return self.repository.create_usuario(
            username=username,
            password_hash=password_hash,
            rol=rol,
            id_estudiante=id_estudiante
        )

    def actualizar_usuario(self, id_usuario, username, password, rol, id_estudiante, activo):
        username = str(username).strip()

        if not username:
            raise ValueError("El username es obligatorio")
        if not password:
            raise ValueError("La contraseña es obligatoria")

        self._validar_rol_estudiante(rol, id_estudiante)

        if id_estudiante is not None:
            self._validar_estudiante_activo(id_estudiante)

        self._validar_username_disponible(username, id_usuario_excluir=id_usuario)

        password_hash = self._hashear_password(password)

        return self.repository.update_usuario(
            id_usuario=id_usuario,
            username=username,
            password_hash=password_hash,
            rol=rol,
            id_estudiante=id_estudiante,
            activo=activo
        )

    def eliminar_usuario(self, id_usuario):
        return self.repository.delete_usuario(id_usuario)


usuario_service = UsuarioService()