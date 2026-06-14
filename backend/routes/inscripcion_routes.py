from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import forbidden_exception, get_current_user, require_admin
from schemas.inscripcion_schema import InscripcionCreate, InscripcionUpdate, InscripcionBaja
from services.inscripcion_service import inscripcion_service

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


@router.get("")
def listar(
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    _=Depends(require_admin),
):
    return {"data": inscripcion_service.listar_inscripciones(fecha_desde, fecha_hasta)}


@router.get("/mias")
def listar_mias(current_user=Depends(get_current_user)):
    if current_user.get("id_estudiante") is None:
        raise forbidden_exception
    return {"data": inscripcion_service.listar_mias(current_user["id_estudiante"])}


@router.get("/{id_inscripcion}")
def obtener(id_inscripcion: int, current_user=Depends(get_current_user)):
    inscripcion = inscripcion_service.obtener_inscripcion(id_inscripcion)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    if current_user["rol"] != "admin" and current_user.get("id_estudiante") != inscripcion["id_estudiante"]:
        raise forbidden_exception
    return {"data": inscripcion}


@router.get("/estudiante/{id_estudiante}")
def listar_por_estudiante(id_estudiante: int, current_user=Depends(get_current_user)):
    if current_user["rol"] != "admin" and current_user.get("id_estudiante") != id_estudiante:
        raise forbidden_exception
    return {"data": inscripcion_service.listar_por_estudiante(id_estudiante)}


@router.get("/practica/{id_practica}")
def listar_por_practica(id_practica: int, _=Depends(require_admin)):
    return {"data": inscripcion_service.listar_por_practica(id_practica)}


@router.post("")
def crear(data: InscripcionCreate, current_user=Depends(get_current_user)):
    id_estudiante = data.id_estudiante
    if current_user["rol"] != "admin":
        if current_user.get("id_estudiante") is None:
            raise forbidden_exception
        if data.id_estudiante != current_user.get("id_estudiante"):
            raise forbidden_exception
        id_estudiante = current_user.get("id_estudiante")

    try:
        id_nuevo = inscripcion_service.crear_inscripcion(
            data.fecha_inscripcion,
            data.estado,
            id_estudiante,
            data.id_practica
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_inscripcion": id_nuevo}}


@router.put("/{id_inscripcion}/estado")
def actualizar_estado(id_inscripcion: int, data: InscripcionUpdate, _=Depends(require_admin)):
    try:
        filas = inscripcion_service.actualizar_estado(id_inscripcion, data.estado)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_inscripcion}")
def dar_baja(id_inscripcion: int, data: InscripcionBaja, current_user=Depends(get_current_user)):
    inscripcion = inscripcion_service.obtener_inscripcion(id_inscripcion)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    if current_user["rol"] != "admin" and current_user.get("id_estudiante") != inscripcion["id_estudiante"]:
        raise forbidden_exception

    try:
        filas = inscripcion_service.dar_baja(id_inscripcion, data.fecha_baja)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return {"data": {"baja": True}}