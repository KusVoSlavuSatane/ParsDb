from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from src.database.session import Base, engine
from src.field.models import Field, FieldCreate
from src.field.service import create as field_create
from src.history.models import History
from src.model.models import Model, ModelCreate
from src.model.service import create as model_create
from src.role.models import Role
from src.user.models import User, UserCreate
from src.user.service import create as user_create


def create_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        # seed roles
        if not session.query(Role).count():
            session.add_all(
                [
                    Role(name="Пользователь"),
                    Role(name="Менеджер"),
                    Role(name="Админ"),
                ]
            )
            session.commit()


def drop_db() -> None:
    Base.metadata.drop_all(bind=engine)


def generate_data(
    db: Session,
):
    ivan = UserCreate(
        name="Иван",
        surname="Бухарин",
        patronymic="Валерьевич",
        role_id=1,
        login="Ivan_Buh",
        password="123",
    )
    valera = UserCreate(
        name="Валерий",
        surname="Лагода",
        patronymic="Юрьевич",
        role_id=2,
        login="lagoda1337",
        password="321",
    )

    field_1 = FieldCreate(
        name="Выручка",
        short_name="В",
        metric="тыс. руб",
    )
    field_2 = FieldCreate(
        name="Среднесписочная численность работающих",
        short_name="ЧР",
        metric="чел.",
    )

    model_1 = ModelCreate(
        name="Модель доходов",
        field_ids=[1],
        analyze_ids=[],
        visible=False,
    )

    user_create(db, ivan)
    user_create(db, valera)
    field_create(db, field_1)
    field_create(db, field_2)
    model_create(db, model_1)
