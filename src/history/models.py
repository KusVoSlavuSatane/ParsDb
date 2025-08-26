from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base

if TYPE_CHECKING:
    from src.model.models import Model
    from src.user.models import User


# ---------- SQLAlchemy ----------
class History(Base):
    __tablename__ = "histories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    period: Mapped[str]
    data: Mapped[dict | None] = mapped_column(JSON)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))

    # user: Mapped["User"] = relationship(back_populates="histories")
    # model_link: Mapped["Model"] = relationship(back_populates="histories_link")


# ---------- Pydantic ----------
class HistoryBase(BaseModel):
    period: str
    data: dict | None = None
    user_id: int
    model_id: int
    model_config = ConfigDict(from_attributes=True)


class HistoryPublic(HistoryBase):
    id: int


class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(HistoryBase):
    pass
