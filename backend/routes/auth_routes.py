from fastapi import APIRouter, Depends
import logging

from core.auth_dependencies import get_current_user
from schemas.auth_schema import LoginRequest
from services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/login")
def login(data: LoginRequest):
    logger.info(f"Login attempt: username={data.username}")
    return {"data": auth_service.login(data.username, data.password)}


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"data": current_user}
