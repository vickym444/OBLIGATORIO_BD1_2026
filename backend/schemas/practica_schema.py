from pydantic import BaseModel


class PracticaCreate(BaseModel):
    id_actividad: int
    fecha: str


class PracticaUpdate(BaseModel):
    id_actividad: int
    fecha: str
    activo: int


class PracticaResponse(BaseModel):
    id_practica: int
    id_actividad: int
    fecha: str
    activo: int