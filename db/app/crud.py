from sqlalchemy.orm import Session
from . import models, schemas

# CRUD операции для всех моделей
def create_entity(db: Session, model, **kwargs):
    db_entity = model(**kwargs)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def get_entity(db: Session, model, entity_id: int):
    return db.query(model).filter(model.id == entity_id).first()

def get_entities(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def delete_entity(db: Session, entity: models.Base):
    db.delete(entity)
    db.commit()

def get_all_entities(db: Session, model: Type[models.Base], skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()