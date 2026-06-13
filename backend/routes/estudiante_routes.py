from fastapi import APIRouter, HTTPException

from services.estudiante_service import estudiante_service

router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])


@router.get("")
def obtener_estudiantes():
    return {"data": estudiante_service.listar_estudiantes()}


@router.get("/{id_estudiante}")
def obtener_estudiante(id_estudiante: int):
    estudiante = estudiante_service.obtener_estudiante(id_estudiante)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"data": estudiante}


@router.post("")
def crear_estudiante(payload: dict):
    estudiante_id = estudiante_service.crear_estudiante(
        documento=payload["documento"],
        nombre=payload["nombre"],
        apellido=payload["apellido"],
        email=payload["email"],
        id_carrera=payload["id_carrera"],
        activo=payload.get("activo", 1),
    )
    return {"id_estudiante": estudiante_id}


@router.put("/{id_estudiante}")
def actualizar_estudiante(id_estudiante: int, payload: dict):
    filas_actualizadas = estudiante_service.actualizar_estudiante(
        id_estudiante=id_estudiante,
        documento=payload["documento"],
        nombre=payload["nombre"],
        apellido=payload["apellido"],
        email=payload["email"],
        activo=payload["activo"],
        id_carrera=payload["id_carrera"],
    )
    if filas_actualizadas == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"updated": filas_actualizadas}


@router.delete("/{id_estudiante}")
def eliminar_estudiante(id_estudiante: int):
    filas_actualizadas = estudiante_service.eliminar_estudiante(id_estudiante)
    if filas_actualizadas == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"deleted": filas_actualizadas}