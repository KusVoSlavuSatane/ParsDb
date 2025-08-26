from fastapi import APIRouter

from src.database.session import SessionDep

from .models import RolePublic
from .service import get_all

roles = APIRouter()


@roles.get("/", response_model=list[RolePublic])
async def get_all_roles(db: SessionDep):
    return get_all(db=db)
