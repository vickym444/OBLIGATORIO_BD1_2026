from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    username: str
    password: str
    rol: str = 'estudiante'
    id_estudiante: Optional[int] = None

class UsuarioUpdate(BaseModel):
    username: str
    password: str
    rol: str
    id_estudiante: Optional[int] = None
    activo: int

class UsuarioResponse(BaseModel):
    id_usuario: int
    username: str
    rol: str
    id_estudiante: Optional[int] = None
    activo: int