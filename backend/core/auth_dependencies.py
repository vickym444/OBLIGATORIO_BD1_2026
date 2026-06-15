from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from core.auth_security import decode_access_token
from repositories.usuario_repository import UsuarioRepository

bearer_scheme = HTTPBearer(auto_error=False)
usuario_repository = UsuarioRepository()

forbidden_exception = HTTPException(
	status_code=status.HTTP_403_FORBIDDEN,
	detail="Acceso denegado",
)


def _unauthorized_exception(detail: str = "No autenticado") -> HTTPException:
	return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
	if credentials is None or not credentials.credentials:
		raise _unauthorized_exception()

	token = credentials.credentials

	try:
		payload = decode_access_token(token)
	except jwt.PyJWTError as exc:
		raise _unauthorized_exception("Token inválido") from exc

	sub = payload.get("sub")
	if not sub:
		raise _unauthorized_exception("Token inválido")

	try:
		id_usuario = int(sub)
	except (TypeError, ValueError) as exc:
		raise _unauthorized_exception("Token inválido") from exc

	usuario = usuario_repository.get_usuario_by_id(id_usuario)
	if not usuario or usuario.get("activo") != 1:
		raise _unauthorized_exception("Usuario no válido")

	return {
		"id_usuario": usuario["id_usuario"],
		"username": usuario["email"],
		"rol": usuario["rol"],
		"id_estudiante": usuario.get("id_estudiante"),
	}


def require_admin(current_user=Depends(get_current_user)):
	if current_user.get("rol") != "admin":
		raise forbidden_exception
	return current_user


def require_estudiante(current_user=Depends(get_current_user)):
	if current_user.get("rol") != "estudiante":
		raise forbidden_exception
	if current_user.get("id_estudiante") is None:
		raise forbidden_exception
	return current_user
