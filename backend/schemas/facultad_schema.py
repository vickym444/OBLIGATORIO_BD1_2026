from pydantic import BaseModel

class FacultadCreate(BaseModel):
    nombre: str

class FacultadUpdate(BaseModel):
    nombre: str
    activo: int

class FacultadResponse(BaseModel):
    id_facultad: int
    nombre: str
    activo: int