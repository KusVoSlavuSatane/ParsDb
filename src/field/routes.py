from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionDep

from .models import FieldCreate, FieldPublic, FieldUpdate
from .service import create, get, get_multi, remove, update

fields = APIRouter()


@fields.get("", response_model=list[FieldPublic])
async def get_all_fields(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    return get_multi(db=db, skip=skip, limit=limit)


@fields.get("/{field_id}", response_model=FieldPublic)
async def get_field(
    db: SessionDep,
    field_id: int,
):
    return get(db=db, field_id=field_id)


@fields.post("/", response_model=FieldPublic)
async def create_field(
    db: SessionDep,
    field_in: FieldCreate,
):
    try:
        field = create(db=db, obj_in=field_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e
    else:
        return field


@fields.patch("/{field_id}", response_model=FieldPublic)
async def update_field(
    db: SessionDep,
    field_id: int,
    field_in: FieldUpdate,
):
    try:
        field = update(db=db, obj_id=field_id, obj_in=field_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    else:
        return field


# Лобавить проверку на то что нельзя удалить если подключено к Model
@fields.delete("/{field_id}", response_model=FieldPublic)
async def delete_field(
    db: SessionDep,
    field_id: int,
):
    try:
        deleted_field = remove(db=db, field_id=field_id)
        if not deleted_field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поле не найдено",
            )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
    else:
        return deleted_field
