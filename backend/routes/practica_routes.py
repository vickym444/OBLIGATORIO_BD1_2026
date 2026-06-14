from fastapi import APIRouter, HTTPException
from schemas.practica_schema import PracticaCreate, PracticaUpdate
from services.practica_service import practica_service

router = APIRouter(prefix="/practicas", tags=["practicas"])


@router.get("")
def listar():
    return {"data": practica_service.listar_practicas()}


@router.get("/actividad/{id_actividad}")
def listar_por_actividad(id_actividad: int):
    return {"data": practica_service.listar_practicas_por_actividad(id_actividad)}


@router.get("/{id_practica}")
def obtener(id_practica: int):
    practica = practica_service.obtener_practica(id_practica)
    if not practica:
        raise HTTPException(status_code=404, detail="Practica no encontrada")
    return {"data": practica}


@router.post("")
def crear(data: PracticaCreate):
    try:
        id_nuevo = practica_service.crear_practica(
            data.id_actividad,
            data.fecha
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_practica": id_nuevo}}


@router.put("/{id_practica}")
def actualizar(id_practica: int, data: PracticaUpdate):
    try:
        filas = practica_service.actualizar_practica(
            id_practica,
            data.id_actividad,
            data.fecha,
            data.activo
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Practica no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_practica}")
def eliminar(id_practica: int):
    filas = practica_service.eliminar_practica(id_practica)
    if not filas:
        raise HTTPException(status_code=404, detail="Practica no encontrada")
    return {"data": {"eliminado": True}}