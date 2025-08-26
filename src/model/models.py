from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base
from src.field.models import FieldPublic, FieldPublicWithotCalc

if TYPE_CHECKING:
    from src.field.models import Field
    from src.history.models import History


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    analyze_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    formula: Mapped[list[str]] = mapped_column(JSON, default=list)
    visible: Mapped[bool] = mapped_column(default=True)

    # histories_link: Mapped[list["History"]] = relationship(back_populates="model_link")
    fields_link: Mapped[list["ModelFields"]] = relationship(
        back_populates="model",
        cascade="all, delete-orphan",  # Будет удалять ModelFields при удалении Model
        passive_deletes=True,
    )

    @property
    def field_ids(self) -> list[int]:
        return [link.field_id for link in self.fields_link]

    @property
    def fields(self) -> list["Field"]:
        return [link.field for link in self.fields_link]


class ModelFields(Base):
    __tablename__ = "model_fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))

    model: Mapped["Model"] = relationship(back_populates="fields_link")
    field: Mapped["Field"] = relationship(back_populates="model_links")


# ---------- Pydantic ----------
class ModelBase(BaseModel):
    name: str
    description: str | None = None
    field_ids: list[int] = []
    analyze_ids: list[str] = []
    formula: list[str] = []
    visible: bool = True
    model_config = ConfigDict(from_attributes=True)


class ModelPublic(ModelBase):
    id: int
    fields: list[FieldPublic] = []


class ModelPublicWithoutCalc(BaseModel):
    fields: list[FieldPublicWithotCalc] = []


class ModelPublicAll(BaseModel):
    id: int
    name: str


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    field_ids: list[int] = []
    analyze_ids: list[str] = []
    formula: list[str] = []
    visible: bool | None = True
