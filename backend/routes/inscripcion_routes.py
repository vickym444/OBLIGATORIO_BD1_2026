from fastapi import APIRouter, HTTPException
from schemas.inscripcion_schema import InscripcionCreate, InscripcionUpdate, InscripcionBaja
from services.inscripcion_service import inscripcion_service

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


@router.get("")
def listar():
    return {"data": inscripcion_service.listar_inscripciones()}


@router.get("/{id_inscripcion}")
def obtener(id_inscripcion: int):
    inscripcion = inscripcion_service.obtener_inscripcion(id_inscripcion)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return {"data": inscripcion}


@router.get("/estudiante/{id_estudiante}")
def listar_por_estudiante(id_estudiante: int):
    return {"data": inscripcion_service.listar_por_estudiante(id_estudiante)}


@router.get("/practica/{id_practica}")
def listar_por_practica(id_practica: int):
    return {"data": inscripcion_service.listar_por_practica(id_practica)}


@router.post("")
def crear(data: InscripcionCreate):
    try:
        id_nuevo = inscripcion_service.crear_inscripcion(
            data.fecha_inscripcion,
            data.estado,
            data.id_estudiante,
            data.id_practica
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_inscripcion": id_nuevo}}


@router.put("/{id_inscripcion}/estado")
def actualizar_estado(id_inscripcion: int, data: InscripcionUpdate):
    try:
        filas = inscripcion_service.actualizar_estado(id_inscripcion, data.estado)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_inscripcion}")
def dar_baja(id_inscripcion: int, data: InscripcionBaja):
    try:
        filas = inscripcion_service.dar_baja(id_inscripcion, data.fecha_baja)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return {"data": {"baja": True}}