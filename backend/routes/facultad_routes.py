from fastapi import APIRouter, HTTPException

from services.facultad_service import facultad_service

router = APIRouter(prefix="/facultades", tags=["facultades"])


@router.get("")
def obtener_facultades():
    return {"data": facultad_service.listar_facultades()}


@router.get("/{id_facultad}")
def obtener_facultad(id_facultad: int):
    facultad = facultad_service.obtener_facultad(id_facultad)
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": facultad}


@router.post("")
def crear_facultad(payload: dict):
    try:
        facultad_id = facultad_service.crear_facultad(nombre=payload.get("nombre", ""))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"id_facultad": facultad_id}


@router.put("/{id_facultad}")
def actualizar_facultad(id_facultad: int, payload: dict):
    try:
        filas_actualizadas = facultad_service.actualizar_facultad(
            id_facultad=id_facultad,
            nombre=payload.get("nombre", ""),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if filas_actualizadas == 0:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    return {"updated": filas_actualizadas}


@router.delete("/{id_facultad}")
def eliminar_facultad(id_facultad: int):
    filas_actualizadas = facultad_service.eliminar_facultad(id_facultad)
    if filas_actualizadas == 0:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"deleted": filas_actualizadas}