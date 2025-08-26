from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base

if TYPE_CHECKING:
    from src.field.models import Field
    from src.user.models import User


# ---------- SQLAlchemy ----------
class UserDataField(Base):
    __tablename__ = "user_data_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[str]
    value: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))

    user: Mapped["User"] = relationship(back_populates="data_fields")
    field: Mapped["Field"] = relationship(back_populates="user_data")


# ---------- Pydantic ----------
class UserDataFieldBase(BaseModel):
    period: str
    value: str
    user_id: int
    field_id: int
    model_config = ConfigDict(from_attributes=True)


class UserDataFieldPublic(UserDataFieldBase):
    id: int


class UserDataFieldCreate(UserDataFieldBase):
    pass


class UserDataFieldUpdate(UserDataFieldBase):
    pass
