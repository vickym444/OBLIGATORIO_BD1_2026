from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    email: str
    password: str
    rol: str = 'estudiante'
    id_estudiante: Optional[int] = None

class UsuarioUpdate(BaseModel):
    email: str
    password: str
    rol: str
    id_estudiante: Optional[int] = None
    activo: int

class UsuarioResponse(BaseModel):
    id_usuario: int
    email: str
    rol: str
    id_estudiante: Optional[int] = None
    activo: int