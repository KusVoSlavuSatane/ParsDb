from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False)  # Фамилия
    name = Column(String, nullable=False)    # Имя
    patronymic = Column(String)              # Отчество
    password = Column(String, nullable=False)
    
    roles = relationship("UserRole", back_populates="user")
    data_fields = relationship("UserDataField", back_populates="user")
    history = relationship("History", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

class Model(Base):
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    args = Column(JSON)  # JSON описание модели
    visible = Column(Boolean, default=False)  # Доступно ли неавторизированным
    
    fields = relationship("ModelFields", back_populates="model")
    history = relationship("History", back_populates="model")

class Field(Base):
    __tablename__ = "fields"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название
    short_name = Column(String)            # Сокращённое название
    metric = Column(String)                # Метрика
    calculation_data = Column(JSON)        # Данные для вычислений (NULL если не вычисляемое)
    
    model_fields = relationship("ModelFields", back_populates="field")
    user_data = relationship("UserDataField", back_populates="field")

class UserDataField(Base):
    __tablename__ = "user_data_fields"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    period = Column(DateTime, default=datetime.utcnow)
    value = Column(String)
    
    user = relationship("User", back_populates="data_fields")
    field = relationship("Field", back_populates="user_data")

class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    period = Column(DateTime, default=datetime.utcnow)
    model_id = Column(Integer, ForeignKey("models.id"))
    data = Column(JSON)  # JSON данные
    
    user = relationship("User", back_populates="history")
    model = relationship("Model", back_populates="history")

class ModelFields(Base):
    __tablename__ = "model_fields"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    
    model = relationship("Model", back_populates="fields")
    field = relationship("Field", back_populates="model_fields")