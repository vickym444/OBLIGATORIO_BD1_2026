from pydantic import BaseModel

class CarreraCreate(BaseModel):
    nombre: str
    id_facultad: int

class CarreraUpdate(BaseModel):
    nombre: str
    id_facultad: int
    activo: int

class CarreraResponse(BaseModel):
    id_carrera: int
    nombre: str
    id_facultad: int
    activo: int