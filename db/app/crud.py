from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from datetime import datetime

# User CRUD
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_name(db: AsyncSession, surname: str, name: str):
    result = await db.execute(
        select(models.User).filter(models.User.surname == surname, models.User.name == name)
    )
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        surname=user.surname,
        name=user.name,
        patronymic=user.patronymic,
        password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Role CRUD
async def get_role(db: AsyncSession, role_id: int):
    result = await db.execute(select(models.Role).filter(models.Role.id == role_id))
    return result.scalars().first()

async def get_role_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Role).filter(models.Role.name == name))
    return result.scalars().first()

async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Role).offset(skip).limit(limit))
    return result.scalars().all()

async def create_role(db: AsyncSession, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

# UserRole CRUD
async def add_user_role(db: AsyncSession, user_id: int, role_id: int):
    db_user_role = models.UserRole(user_id=user_id, role_id=role_id)
    db.add(db_user_role)
    await db.commit()
    await db.refresh(db_user_role)
    return db_user_role

async def get_user_roles(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Role)
        .join(models.UserRole)
        .filter(models.UserRole.user_id == user_id)
    )
    return result.scalars().all()

# Model CRUD
async def get_model(db: AsyncSession, model_id: int):
    result = await db.execute(select(models.Model).filter(models.Model.id == model_id))
    return result.scalars().first()

async def get_models(db: AsyncSession, skip: int = 0, limit: int = 100, visible_only: bool = False):
    query = select(models.Model)
    if visible_only:
        query = query.filter(models.Model.visible == True)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def create_model(db: AsyncSession, model: schemas.ModelCreate):
    db_model = models.Model(
        name=model.name,
        description=model.description,
        args=model.args,
        visible=model.visible
    )
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model

# Field CRUD
async def get_field(db: AsyncSession, field_id: int):
    result = await db.execute(select(models.Field).filter(models.Field.id == field_id))
    return result.scalars().first()

async def get_fields(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Field).offset(skip).limit(limit))
    return result.scalars().all()

async def create_field(db: AsyncSession, field: schemas.FieldCreate):
    db_field = models.Field(
        name=field.name,
        short_name=field.short_name,
        metric=field.metric,
        calculation_data=field.calculation_data
    )
    db.add(db_field)
    await db.commit()
    await db.refresh(db_field)
    return db_field

# UserDataField CRUD
async def get_user_data(db: AsyncSession, user_id: int, field_id: int = None):
    query = select(models.UserDataField).filter(models.UserDataField.user_id == user_id)
    if field_id:
        query = query.filter(models.UserDataField.field_id == field_id)
    result = await db.execute(query)
    return result.scalars().all()

async def create_user_data(db: AsyncSession, user_data: schemas.UserDataFieldCreate):
    db_user_data = models.UserDataField(
        user_id=user_data.user_id,
        field_id=user_data.field_id,
        value=user_data.value,
        period=user_data.period or datetime.utcnow()
    )
    db.add(db_user_data)
    await db.commit()
    await db.refresh(db_user_data)
    return db_user_data

# History CRUD
async def get_history(db: AsyncSession, user_id: int = None, model_id: int = None):
    query = select(models.History)
    if user_id:
        query = query.filter(models.History.user_id == user_id)
    if model_id:
        query = query.filter(models.History.model_id == model_id)
    result = await db.execute(query)
    return result.scalars().all()

async def create_history(db: AsyncSession, history: schemas.HistoryCreate):
    db_history = models.History(
        user_id=history.user_id,
        model_id=history.model_id,
        data=history.data,
        period=history.period or datetime.utcnow()
    )
    db.add(db_history)
    await db.commit()
    await db.refresh(db_history)
    return db_history

# ModelFields CRUD
async def add_model_field(db: AsyncSession, model_field: schemas.ModelFieldsCreate):
    db_model_field = models.ModelFields(
        model_id=model_field.model_id,
        field_id=model_field.field_id
    )
    db.add(db_model_field)
    await db.commit()
    await db.refresh(db_model_field)
    return db_model_field

async def get_model_fields(db: AsyncSession, model_id: int):
    result = await db.execute(
        select(models.Field)
        .join(models.ModelFields)
        .filter(models.ModelFields.model_id == model_id)
    )
    return result.scalars().all()