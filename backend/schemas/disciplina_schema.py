from pydantic import BaseModel
from typing import Optional

class DisciplinaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class DisciplinaUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: int

class DisciplinaResponse(BaseModel):
    id_disciplina: int
    nombre: str
    descripcion: Optional[str] = None
    activo: int