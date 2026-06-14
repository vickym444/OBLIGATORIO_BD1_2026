from typing import List

from pydantic import BaseModel, Field


class AsistenciaCreate(BaseModel):
    presente: int
    id_inscripcion: int


class AsistenciaUpdate(BaseModel):
    presente: int


class AsistenciaResponse(BaseModel):
    id_asistencia: int
    presente: int
    id_inscripcion: int


class AsistenciaRegistro(BaseModel):
    id_inscripcion: int
    presente: bool = False


class AsistenciaLoteCreate(BaseModel):
    registros: List[AsistenciaRegistro] = Field(default_factory=list)