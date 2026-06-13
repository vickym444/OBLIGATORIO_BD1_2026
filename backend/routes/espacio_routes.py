from fastapi import APIRouter, HTTPException
from schemas.espacio_schema import EspacioCreate, EspacioUpdate
from services.espacio_service import espacio_service

router = APIRouter(prefix="/espacios", tags=["espacios"])


@router.get("")
def listar():
    return {"data": espacio_service.listar_espacios()}


@router.get("/{id_espacio}")
def obtener(id_espacio: int):
    espacio = espacio_service.obtener_espacio(id_espacio)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": espacio}


@router.post("")
def crear(data: EspacioCreate):
    id_nuevo = espacio_service.crear_espacio(data.nombre, data.descripcion)
    return {"data": {"id_espacio": id_nuevo}}


@router.put("/{id_espacio}")
def actualizar(id_espacio: int, data: EspacioUpdate):
    filas = espacio_service.actualizar_espacio(
        id_espacio, data.nombre, data.descripcion, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": {"actualizado": True}}


@router.delete("/{id_espacio}")
def eliminar(id_espacio: int):
    filas = espacio_service.eliminar_espacio(id_espacio)
    if not filas:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": {"eliminado": True}}