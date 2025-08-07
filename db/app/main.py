from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app import crud, models, schemas
from app.database import get_db, init_models
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_models()

# Users endpoints
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_name(db, surname=user.surname, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return await crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserWithRoles)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    roles = await crud.get_user_roles(db, user_id=user_id)
    return {**db_user.__dict__, "roles": roles}

# Roles endpoints
@app.post("/roles/", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: AsyncSession = Depends(get_db)):
    db_role = await crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return await crud.create_role(db=db, role=role)

@app.get("/roles/", response_model=List[schemas.Role])
async def read_roles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    roles = await crud.get_roles(db, skip=skip, limit=limit)
    return roles

@app.post("/users/{user_id}/roles/{role_id}", response_model=schemas.UserWithRoles)
async def add_role_to_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    await crud.add_user_role(db=db, user_id=user_id, role_id=role_id)
    return await read_user(user_id=user_id, db=db)

# Models endpoints
@app.post("/models/", response_model=schemas.Model)
async def create_model(model: schemas.ModelCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_model(db=db, model=model)

@app.get("/models/", response_model=List[schemas.Model])
async def read_models(skip: int = 0, limit: int = 100, visible_only: bool = False, db: AsyncSession = Depends(get_db)):
    models = await crud.get_models(db, skip=skip, limit=limit, visible_only=visible_only)
    return models

@app.get("/models/{model_id}", response_model=schemas.ModelWithFields)
async def read_model(model_id: int, db: AsyncSession = Depends(get_db)):
    db_model = await crud.get_model(db, model_id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    fields = await crud.get_model_fields(db, model_id=model_id)
    return {**db_model.__dict__, "fields": fields}

# Fields endpoints
@app.post("/fields/", response_model=schemas.Field)
async def create_field(field: schemas.FieldCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_field(db=db, field=field)

@app.get("/fields/", response_model=List[schemas.Field])
async def read_fields(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    fields = await crud.get_fields(db, skip=skip, limit=limit)
    return fields

@app.post("/models/{model_id}/fields/{field_id}", response_model=schemas.ModelWithFields)
async def add_field_to_model(model_id: int, field_id: int, db: AsyncSession = Depends(get_db)):
    await crud.add_model_field(db=db, model_field=schemas.ModelFieldsCreate(model_id=model_id, field_id=field_id))
    return await read_model(model_id=model_id, db=db)

# UserData endpoints
@app.post("/user-data/", response_model=schemas.UserDataField)
async def create_user_data(user_data: schemas.UserDataFieldCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user_data(db=db, user_data=user_data)

@app.get("/users/{user_id}/data/", response_model=List[schemas.UserDataField])
async def read_user_data(user_id: int, field_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_data(db, user_id=user_id, field_id=field_id)

# History endpoints
@app.post("/history/", response_model=schemas.History)
async def create_history(history: schemas.HistoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_history(db=db, history=history)

@app.get("/history/", response_model=List[schemas.History])
async def read_history(user_id: int = None, model_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_history(db, user_id=user_id, model_id=model_id)