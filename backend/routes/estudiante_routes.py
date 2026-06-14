from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.estudiante_schema import EstudianteCreate, EstudianteUpdate
from services.estudiante_service import estudiante_service as service

router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": service.listar_estudiantes()}


@router.get("/{id_estudiante}")
def obtener(id_estudiante: int, _=Depends(require_admin)):
    estudiante = service.obtener_estudiante(id_estudiante)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"data": estudiante}


@router.post("")
def crear(data: EstudianteCreate, _=Depends(require_admin)):
    try:
        id_nuevo = service.crear_estudiante(
            data.documento,
            data.nombre,
            data.apellido,
            data.email,
            data.id_carrera
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_estudiante": id_nuevo}}


@router.put("/{id_estudiante}")
def actualizar(id_estudiante: int, data: EstudianteUpdate, _=Depends(require_admin)):
    try:
        filas = service.actualizar_estudiante(
            id_estudiante,
            data.documento,
            data.nombre,
            data.apellido,
            data.email,
            data.activo,
            data.id_carrera
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"data": {"actualizado": True}}


@router.delete("/{id_estudiante}")
def eliminar(id_estudiante: int, _=Depends(require_admin)):
    filas = service.eliminar_estudiante(id_estudiante)
    if not filas:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"data": {"eliminado": True}}