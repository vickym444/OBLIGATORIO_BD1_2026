from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from services.usuario_service import usuario_service as service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": service.listar_usuarios()}


@router.get("/{id_usuario}")
def obtener(id_usuario: int, _=Depends(require_admin)):
    usuario = service.obtener_usuario(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"data": usuario}


@router.post("")
def crear(data: UsuarioCreate, _=Depends(require_admin)):
    try:
        id_nuevo = service.crear_usuario(
            data.username,
            data.password,
            data.rol,
            data.id_estudiante
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_usuario": id_nuevo}}


@router.put("/{id_usuario}")
def actualizar(id_usuario: int, data: UsuarioUpdate, _=Depends(require_admin)):
    try:
        filas = service.actualizar_usuario(
            id_usuario,
            data.username,
            data.password,
            data.rol,
            data.id_estudiante,
            data.activo
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"data": {"actualizado": True}}


@router.delete("/{id_usuario}")
def eliminar(id_usuario: int, _=Depends(require_admin)):
    filas = service.eliminar_usuario(id_usuario)
    if not filas:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"data": {"eliminado": True}}