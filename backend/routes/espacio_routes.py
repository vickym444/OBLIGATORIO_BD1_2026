from fastapi import APIRouter, HTTPException
from schemas.espacio_schema import EspacioCreate, EspacioUpdate
import services.espacio_service as service

router = APIRouter(prefix="/espacios", tags=["espacios"])


@router.get("")
def listar():
    return {"data": service.listar_espacios()}


@router.get("/{id_espacio}")
def obtener(id_espacio: int):
    espacio = service.obtener_espacio(id_espacio)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": espacio}


@router.post("")
def crear(data: EspacioCreate):
    id_nuevo = service.crear_espacio(data.nombre, data.descripcion)
    return {"data": {"id_espacio": id_nuevo}}


@router.put("/{id_espacio}")
def actualizar(id_espacio: int, data: EspacioUpdate):
    filas = service.actualizar_espacio(
        id_espacio, data.nombre, data.descripcion, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": {"actualizado": True}}


@router.delete("/{id_espacio}")
def eliminar(id_espacio: int):
    filas = service.eliminar_espacio(id_espacio)
    if not filas:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return {"data": {"eliminado": True}}