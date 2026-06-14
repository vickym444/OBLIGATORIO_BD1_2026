from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.actividad_schema import ActividadCreate, ActividadUpdate
from services.actividad_service import actividad_service

router = APIRouter(prefix="/actividades", tags=["actividades"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": actividad_service.listar_actividades()}


@router.get("/{id_actividad}")
def obtener(id_actividad: int, _=Depends(require_admin)):
    actividad = actividad_service.obtener_actividad(id_actividad)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return {"data": actividad}


@router.post("")
def crear(data: ActividadCreate, _=Depends(require_admin)):
    try:
        id_nuevo = actividad_service.crear_actividad(
            data.nombre,
            data.cupo_maximo,
            data.cupo_minimo,
            data.hora_inicio,
            data.hora_fin,
            data.dia,
            data.estado,
            data.id_disciplina,
            data.id_espacio
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_actividad": id_nuevo}}


@router.put("/{id_actividad}")
def actualizar(id_actividad: int, data: ActividadUpdate, _=Depends(require_admin)):
    try:
        filas = actividad_service.actualizar_actividad(
            id_actividad,
            data.nombre,
            data.cupo_maximo,
            data.cupo_minimo,
            data.hora_inicio,
            data.hora_fin,
            data.dia,
            data.estado,
            data.id_disciplina,
            data.id_espacio,
            data.activo
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_actividad}")
def eliminar(id_actividad: int, _=Depends(require_admin)):
    filas = actividad_service.eliminar_actividad(id_actividad)
    if not filas:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return {"data": {"eliminado": True}}