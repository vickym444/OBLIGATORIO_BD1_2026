from fastapi import HTTPException, status

from core.auth_security import create_access_token, verify_password
from repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()

    def login(self, username, password):
        username = str(username).strip()
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username y contraseña son obligatorios",
            )

        usuario = self.repository.get_usuario_auth_by_username(username)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        if usuario.get("activo") != 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
            )

        password_ok = verify_password(password, usuario.get("password_hash", ""))
        if not password_ok:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        token = create_access_token(
            {
                "sub": str(usuario["id_usuario"]),
                "rol": usuario["rol"],
                "id_estudiante": usuario.get("id_estudiante"),
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id_usuario": usuario["id_usuario"],
                "username": usuario["email"],
                "rol": usuario["rol"],
                "id_estudiante": usuario.get("id_estudiante"),
            },
        }


auth_service = AuthService()
