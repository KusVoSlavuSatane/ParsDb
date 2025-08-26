from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base

if TYPE_CHECKING:
    from src.role.models import Role


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    @property
    def role_name(self) -> str:
        return self.role.name if self.role else None


# ---------- Pydantic схемы ----------


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str | None = None
    role_id: int
    login: str

    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserBase):
    id: int
    role_name: str | None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    role_id: int | None = None
    login: str | None = None


class UserUpdatePass(BaseModel):
    password: str
