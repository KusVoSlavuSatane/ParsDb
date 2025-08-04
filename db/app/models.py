from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    
    role = relationship("Role", back_populates="users")
    data_fields = relationship("UserDataField", back_populates="user")
    histories = relationship("History", back_populates="user")

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    users = relationship("User", back_populates="role")

class Model(Base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    argu_json = Column(JSON)
    visible = Column(Boolean, default=False)
    
    histories = relationship("History", back_populates="model")

class Field(Base):
    __tablename__ = 'fields'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    short_name = Column(String)
    metric = Column(String)
    computed = Column(Integer)
    
    user_data_fields = relationship("UserDataField", back_populates="field")

class UserDataField(Base):
    __tablename__ = 'user_data_fields'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    field_id = Column(Integer, ForeignKey('fields.id'))
    period = Column(String)
    value = Column(String)
    
    user = relationship("User", back_populates="data_fields")
    field = relationship("Field", back_populates="user_data_fields")

class History(Base):
    __tablename__ = 'histories'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    period = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))
    data = Column(JSON)
    
    user = relationship("User", back_populates="histories")
    model = relationship("Model", back_populates="histories")