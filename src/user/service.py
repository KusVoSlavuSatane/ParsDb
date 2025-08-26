from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from src.user.models import User, UserCreate, UserUpdate, UserUpdatePass


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get(db: Session, user_id: int) -> User | None:
    try:
        return db.get(User, user_id, options=[selectinload(User.role)])
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def create(db: Session, user_in: UserCreate) -> User:
    try:
        user = User(**user_in.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return user


def update(db: Session, user_id: int, user_in: UserUpdate | UserUpdatePass) -> User:
    try:
        user = get(db, user_id)
        for field, value in user_in.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return user


def delete(db: Session, user_id: int) -> User | None:
    try:
        user = get(db, user_id)
        if user is None:
            return None
        db.delete(user)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    else:
        return user
