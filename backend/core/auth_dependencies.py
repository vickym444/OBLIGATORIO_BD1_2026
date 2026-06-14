import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.auth_security import decode_access_token
from repositories.usuario_repository import UsuarioRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthUser(dict):
    @property
    def id_usuario(self):
        return self.get("id_usuario")

    @property
    def username(self):
        return self.get("username")

    @property
    def rol(self):
        return self.get("rol")

    @property
    def id_estudiante(self):
        return self.get("id_estudiante")


unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autenticado",
    headers={"WWW-Authenticate": "Bearer"},
)


forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tienes permisos para esta operación",
)


def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthUser:
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError as exc:
        raise unauthorized_exception from exc

    id_usuario = payload.get("sub")
    if id_usuario is None:
        raise unauthorized_exception

    repo = UsuarioRepository()
    usuario = repo.get_usuario_by_id(int(id_usuario))
    if not usuario or usuario.get("activo") != 1:
        raise unauthorized_exception

    return AuthUser(usuario)


def require_admin(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if current_user.rol != "admin":
        raise forbidden_exception
    return current_user
