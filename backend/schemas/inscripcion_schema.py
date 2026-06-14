from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum


class EstadoInscripcionEnum(str, Enum):
    confirmada = "confirmada"
    en_espera = "en_espera"
    cancelada = "cancelada"


class InscripcionCreate(BaseModel):
    fecha_inscripcion: date
    estado: Optional[EstadoInscripcionEnum] = None
    id_estudiante: int
    id_practica: int


class InscripcionUpdate(BaseModel):
    estado: EstadoInscripcionEnum


class InscripcionBaja(BaseModel):
    fecha_baja: date


class InscripcionResponse(BaseModel):
    id_inscripcion: int
    fecha_inscripcion: date
    fecha_baja: Optional[date] = None
    estado: str
    id_estudiante: int
    id_practica: int