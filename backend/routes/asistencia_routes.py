from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.asistencia_schema import AsistenciaCreate, AsistenciaUpdate, AsistenciaLoteCreate
from services.asistencia_service import asistencia_service

router = APIRouter(prefix="/asistencias", tags=["asistencias"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": asistencia_service.listar_asistencias()}


@router.get("/rango")
def listar_por_rango(
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    _=Depends(require_admin),
):
    return {"data": asistencia_service.listar_practicas_para_asistencia(fecha_desde, fecha_hasta)}


@router.get("/{id_asistencia}")
def obtener(id_asistencia: int, _=Depends(require_admin)):
    asistencia = asistencia_service.obtener_asistencia(id_asistencia)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return {"data": asistencia}


@router.get("/inscripcion/{id_inscripcion}")
def obtener_por_inscripcion(id_inscripcion: int, _=Depends(require_admin)):
    asistencia = asistencia_service.obtener_por_inscripcion(id_inscripcion)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return {"data": asistencia}


@router.post("")
def registrar(data: AsistenciaCreate, _=Depends(require_admin)):
    try:
        id_nuevo = asistencia_service.registrar_asistencia(
            data.presente,
            data.id_inscripcion
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_asistencia": id_nuevo}}


@router.post("/lote")
def registrar_lote(data: AsistenciaLoteCreate, _=Depends(require_admin)):
    try:
        filas = asistencia_service.guardar_asistencias_lote(data.registros)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"guardadas": filas}}


@router.put("/{id_asistencia}")
def actualizar(id_asistencia: int, data: AsistenciaUpdate, _=Depends(require_admin)):
    try:
        filas = asistencia_service.actualizar_asistencia(id_asistencia, data.presente)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return {"data": {"actualizado": True}}