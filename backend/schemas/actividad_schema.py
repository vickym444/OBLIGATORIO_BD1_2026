from pydantic import BaseModel
from typing import Optional
from enum import Enum


class DiaEnum(str, Enum):
    lunes = "Lunes"
    martes = "Martes"
    miercoles = "Miercoles"
    jueves = "Jueves"
    viernes = "Viernes"
    lunes_miercoles = "Lunes y Miercoles"
    martes_jueves = "Martes y Jueves"
    miercoles_viernes = "Miercoles y Viernes"


class EstadoEnum(str, Enum):
    abierta = "abierta"
    cerrada = "cerrada"
    finalizada = "finalizada"
    cancelada = "cancelada"


class ActividadCreate(BaseModel):
    nombre: str
    cupo_maximo: int
    cupo_minimo: int
    hora_inicio: str
    hora_fin: str
    dia: DiaEnum
    estado: EstadoEnum
    id_disciplina: int
    id_espacio: int


class ActividadUpdate(BaseModel):
    nombre: str
    cupo_maximo: int
    cupo_minimo: int
    hora_inicio: str
    hora_fin: str
    dia: DiaEnum
    estado: EstadoEnum
    id_disciplina: int
    id_espacio: int
    activo: int


class ActividadResponse(BaseModel):
    id_actividad: int
    nombre: str
    cupo_maximo: int
    cupo_minimo: int
    hora_inicio: str
    hora_fin: str
    dia: str
    estado: str
    id_disciplina: int
    id_espacio: int
    activo: int