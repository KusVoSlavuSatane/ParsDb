from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.field.models import Field, FieldCreate, FieldUpdate


def get(db: Session, field_id: int) -> Field | None:
    try:
        return db.get(Field, field_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Field]:
    try:
        return db.query(Field).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def create(db: Session, obj_in: FieldCreate) -> Field:
    try:
        obj = Field(**obj_in.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
    except SQLAlchemyError as e:
        db.rollback()
    else:
        return obj


def update(db: Session, obj_id: int, obj_in: FieldUpdate) -> Field:
    try:
        db_obj = get(db, obj_id)
        if not db:
            return None
        updated_data = obj_in.model_dump(exclude_unset=True)
        for field, value in updated_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return db_obj


def remove(db: Session, field_id: int) -> Field | None:
    try:
        obj = get(db, field_id)
        if obj:
            db.delete(obj)
            db.commit()
    except IntegrityError as e:
        db.rollback()
        # Это может произойти при нарушении ограничений внешних ключей
        msg = f"Невозможно удалить поле, так как оно используется в моделях: {e}"
        raise ValueError(
            msg,
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return obj
