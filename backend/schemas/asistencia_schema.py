from pydantic import BaseModel


class AsistenciaCreate(BaseModel):
    presente: int
    id_inscripcion: int


class AsistenciaUpdate(BaseModel):
    presente: int


class AsistenciaResponse(BaseModel):
    id_asistencia: int
    presente: int
    id_inscripcion: int