from sqlalchemy import and_, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, selectinload

from src.field.models import Field

from .models import Model, ModelCreate, ModelFields, ModelUpdate


def get(db: Session, obj_id: int) -> Model | None:
    try:
        return db.get(
            Model,
            obj_id,
            options=[selectinload(Model.fields_link).joinedload(ModelFields.field)],
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_user(db: Session, obj_id: int) -> Model | None:
    try:
        model = db.query(Model).filter(Model.id == obj_id).first()
        if not model:
            return None
        model_fields = (
            db.query(ModelFields)
            .join(Field)
            .filter(
                and_(
                    ModelFields.model_id == obj_id,
                    or_(
                        Field.calc_data.is_(None),
                        Field.calc_data == "[]",
                        Field.calc_data == [],
                    ),
                ),
            )
            .options(joinedload(ModelFields.field))
            .all()
        )

        model.fields_link = model_fields

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return model


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Model]:
    try:
        return (
            db.query(Model)
            .options(
                selectinload(Model.fields_link).joinedload(ModelFields.field),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def create(db: Session, obj_in: ModelCreate) -> Model:
    try:
        # Извлекаем field_ids заранее
        field_ids = obj_in.field_ids or []
        create_data = obj_in.model_dump(exclude={"field_ids"})

        # Создаем модель без field_ids
        db_obj = Model(**create_data)
        db.add(db_obj)
        db.flush()  # Получаем ID без коммита

        # Устанавливаем связи отдельно
        if field_ids:
            # Ручная установка связей
            for field_id in field_ids:
                model_field = ModelFields(model_id=db_obj.id, field_id=field_id)
                db_obj.fields_link.append(model_field)

        db.commit()
        db.refresh(db_obj)

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return db_obj


def update(db: Session, model_id: int, obj_in: ModelUpdate) -> Model | None:
    try:
        db_obj = get(db, model_id)
        if not db_obj:
            return None

        # Получаем данные для обновления
        update_data = obj_in.model_dump(exclude_unset=True, exclude={"field_ids"})
        field_ids = getattr(obj_in, "field_ids", None)

        # Обновляем основные поля
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Обновляем связи с полями если переданы
        if field_ids is not None:
            # Очищаем старые связи
            db_obj.fields_link.clear()
            # Добавляем новые
            for field_id in field_ids:
                model_field = ModelFields(model_id=db_obj.id, field_id=field_id)
                db_obj.fields_link.append(model_field)

        db.commit()
        db.refresh(db_obj)

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return db_obj


def remove(db: Session, model_id: int) -> Model | None:
    try:
        obj = get(db, model_id)
        if not obj:
            raise ValueError(f"Такого нет {model_id}")
        db.delete(obj)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return obj
