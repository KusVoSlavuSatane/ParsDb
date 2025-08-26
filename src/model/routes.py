from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionDep
from src.logging_config import logger

from .models import ModelCreate, ModelPublic, ModelPublicAll, ModelPublicWithoutCalc, ModelUpdate
from .service import create, get, get_multi, get_user, remove, update

models = APIRouter()


@models.post("/", response_model=ModelPublic)
async def create_model(
    db: SessionDep,
    obj_in: ModelCreate,
):
    try:
        model = create(db=db, obj_in=obj_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e
    else:
        return model


@models.get("/{obj_id}", response_model=ModelPublic)
async def get_model(
    db: SessionDep,
    obj_id: int,
):
    try:
        model = get(db=db, obj_id=obj_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model Not Found {obj_id}",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=(str(e))) from e
    else:
        return model


@models.get("/user_fields/{obj_id}", response_model=ModelPublicWithoutCalc)
async def get_user_model(
    db: SessionDep,
    obj_id: int,
):
    try:
        model = get_user(db=db, obj_id=obj_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model Not Found {obj_id}",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=(str(e))) from e
    else:
        return model


@models.get("/", response_model=list[ModelPublicAll])
async def get_models(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    try:
        models = get_multi(db, skip, limit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    else:
        return models


@models.patch("/{model_id}", response_model=ModelPublic)
async def update_model(
    db: SessionDep,
    model_id: int,
    model_in: ModelUpdate,
):
    try:
        model = update(db, model_id, model_in)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Такой модели нет",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    else:
        return model


@models.delete("/{model_id}", response_model=ModelPublic)
async def remove_model(db: SessionDep, model_id: int):
    try:
        model = remove(db, model_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Такой модели нет",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    else:
        return model
