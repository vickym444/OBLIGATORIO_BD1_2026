from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.disciplina_schema import DisciplinaCreate, DisciplinaUpdate
from services.disciplina_service import disciplina_service

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": disciplina_service.listar_disciplinas()}


@router.get("/{id_disciplina}")
def obtener(id_disciplina: int, _=Depends(require_admin)):
    disciplina = disciplina_service.obtener_disciplina(id_disciplina)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": disciplina}


@router.post("")
def crear(data: DisciplinaCreate, _=Depends(require_admin)):
    try:
        id_nuevo = disciplina_service.crear_disciplina(data.nombre, data.descripcion)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"data": {"id_disciplina": id_nuevo}}


@router.put("/{id_disciplina}")
def actualizar(id_disciplina: int, data: DisciplinaUpdate, _=Depends(require_admin)):
    filas = disciplina_service.actualizar_disciplina(
        id_disciplina, data.nombre, data.descripcion, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_disciplina}")
def eliminar(id_disciplina: int, _=Depends(require_admin)):
    filas = disciplina_service.eliminar_disciplina(id_disciplina)
    if not filas:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": {"eliminado": True}}