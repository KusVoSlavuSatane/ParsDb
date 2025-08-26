from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base

if TYPE_CHECKING:
    from src.model.models import ModelFields
    from src.user_data_fields.models import UserDataField


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    short_name: Mapped[str]
    metric: Mapped[str | None] = mapped_column(nullable=True)
    calc_data: Mapped[list[str]] = mapped_column(JSON, default=lambda: [], nullable=False)

    # user_data: Mapped[list["UserDataField"]] = relationship(back_populates="field")
    model_links: Mapped[list["ModelFields"]] = relationship(
        back_populates="field",
        cascade="all, delete-orphan",
    )


class FieldBase(BaseModel):
    name: str
    short_name: str
    metric: str | None = None
    calc_data: list[str] = []
    model_config = ConfigDict(from_attributes=True)


class FieldPublic(FieldBase):
    id: int


class FieldPublicWithotCalc(BaseModel):
    id: int
    name: str
    short_name: str
    metric: str | None = None
    model_config = ConfigDict(from_attributes=True)


class FieldCreate(FieldBase):
    pass


class FieldUpdate(BaseModel):
    name: str | None = None
    short_name: str | None = None
    metric: str | None = None
    calc_data: list[str] | None = None  # Может быть None при частичном обновлении
    model_config = ConfigDict(from_attributes=True)
