from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionDep

from .models import UserCreate, UserPublic, UserUpdate, UserUpdatePass
from .service import create, delete, get, get_multi, update

users = APIRouter()


@users.get("/", response_model=list[UserPublic])
async def get_all_users(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    try:
        users = get_multi(db=db, skip=skip, limit=limit)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    else:
        return users


@users.get("/{user_id}", response_model=UserPublic)
async def get_user(
    db: SessionDep,
    user_id: int,
):
    user = get(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user


@users.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    db: SessionDep,
    user_in: UserCreate,
):
    try:
        user = create(db, user_in=user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    else:
        return user


@users.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    db: SessionDep,
    user_id: int,
    user_update: UserUpdate,
):
    try:
        updated_user = update(db, user_id=user_id, user_in=user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return updated_user


@users.put("/{user_id}", response_model=UserUpdatePass)
async def update_password(
    db: SessionDep,
    user_id: int,
    password: UserUpdatePass,
):
    try:
        updated_pass = update(db, user_id, password)
        if not updated_pass:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return updated_pass


@users.delete("/{user_id}", response_model=UserPublic)
async def delete_user(
    user_id: int,
    db: SessionDep,
):
    deleted_user = delete(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return deleted_user
