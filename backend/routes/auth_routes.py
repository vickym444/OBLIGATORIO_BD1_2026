from fastapi import APIRouter, Depends

from core.auth_dependencies import get_current_user
from schemas.auth_schema import LoginRequest
from services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(data: LoginRequest):
    return {"data": auth_service.login(data.username, data.password)}


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"data": current_user}
