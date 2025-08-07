from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

# Базовые схемы
class UserBase(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None

class RoleBase(BaseModel):
    name: str

class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    visible: bool = False

class FieldBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    metric: Optional[str] = None
    calculation_data: Optional[Dict[str, Any]] = None

# Схемы для создания
class UserCreate(UserBase):
    password: str

class RoleCreate(RoleBase):
    pass

class ModelCreate(ModelBase):
    pass

class FieldCreate(FieldBase):
    pass

class UserDataFieldCreate(BaseModel):
    user_id: int
    field_id: int
    value: str
    period: Optional[datetime] = None

class HistoryCreate(BaseModel):
    user_id: int
    model_id: int
    data: Dict[str, Any]
    period: Optional[datetime] = None

class ModelFieldsCreate(BaseModel):
    model_id: int
    field_id: int

# Схемы для ответов
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class Role(RoleBase):
    id: int
    
    class Config:
        orm_mode = True

class Model(ModelBase):
    id: int
    
    class Config:
        orm_mode = True

class Field(FieldBase):
    id: int
    
    class Config:
        orm_mode = True

class UserDataField(BaseModel):
    id: int
    user_id: int
    field_id: int
    period: datetime
    value: str
    
    class Config:
        orm_mode = True

class History(BaseModel):
    id: int
    user_id: int
    period: datetime
    model_id: int
    data: Dict[str, Any]
    
    class Config:
        orm_mode = True

class ModelFields(BaseModel):
    id: int
    model_id: int
    field_id: int
    
    class Config:
        orm_mode = True

# Схемы с отношениями
class UserWithRoles(User):
    roles: List[Role] = []

class RoleWithUsers(Role):
    users: List[User] = []

class ModelWithFields(Model):
    fields: List[Field] = []

class FieldWithModels(Field):
    models: List[Model] = []