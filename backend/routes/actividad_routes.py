from fastapi import APIRouter

from services.actividad_service import listar_actividades

router = APIRouter(prefix="/actividades", tags=["actividades"])


@router.get("")
def obtener_actividades():
    return {"data": listar_actividades()}