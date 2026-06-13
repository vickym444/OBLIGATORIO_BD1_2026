from fastapi import APIRouter, HTTPException
from schemas.disciplina_schema import DisciplinaCreate, DisciplinaUpdate
import services.disciplina_service as service

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get("")
def listar():
    return {"data": service.listar_disciplinas()}


@router.get("/{id_disciplina}")
def obtener(id_disciplina: int):
    disciplina = service.obtener_disciplina(id_disciplina)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": disciplina}


@router.post("")
def crear(data: DisciplinaCreate):
    id_nuevo = service.crear_disciplina(data.nombre, data.descripcion)
    return {"data": {"id_disciplina": id_nuevo}}


@router.put("/{id_disciplina}")
def actualizar(id_disciplina: int, data: DisciplinaUpdate):
    filas = service.actualizar_disciplina(
        id_disciplina, data.nombre, data.descripcion, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_disciplina}")
def eliminar(id_disciplina: int):
    filas = service.eliminar_disciplina(id_disciplina)
    if not filas:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return {"data": {"eliminado": True}}