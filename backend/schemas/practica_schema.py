from datetime import date

from pydantic import BaseModel


class PracticaCreate(BaseModel):
    id_actividad: int
    fecha: date


class PracticaUpdate(BaseModel):
    id_actividad: int
    fecha: date
    activo: int


class PracticaResponse(BaseModel):
    id_practica: int
    id_actividad: int
    fecha: date
    activo: int