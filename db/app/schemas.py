from pydantic import BaseModel
from typing import Optional, Dict, Any

# Общие схемы
class RoleBase(BaseModel):
    name: str

class UserBase(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    role_id: int

class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    argu_json: Optional[Dict[str, Any]] = None
    visible: bool = False

class FieldBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    metric: Optional[str] = None

# Схемы для создания
class UserCreate(UserBase):
    password: str

class UserDataFieldCreate(BaseModel):
    user_id: int
    field_id: int
    period: str
    value: str

class HistoryCreate(BaseModel):
    user_id: int
    period: str
    model_id: int
    data: Dict[str, Any]

# Схемы ответов
class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Role(RoleBase):
    id: int
    class Config:
        from_attributes = True

class Model(ModelBase):
    id: int
    class Config:
        from_attributes = True

class Field(FieldBase):
    id: int
    class Config:
        from_attributes = True

class UserDataField(UserDataFieldCreate):
    id: int
    class Config:
        from_attributes = True

class History(HistoryCreate):
    id: int
    class Config:
        from_attributes = True