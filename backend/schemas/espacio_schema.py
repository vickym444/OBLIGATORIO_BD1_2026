from pydantic import BaseModel
from typing import Optional

class EspacioCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EspacioUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: int

class EspacioResponse(BaseModel):
    id_espacio: int
    nombre: str
    descripcion: Optional[str] = None
    activo: int