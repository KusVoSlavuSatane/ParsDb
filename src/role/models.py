from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base

if TYPE_CHECKING:
    from src.user.models import User


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


# ---------- Pydantic схемы ----------
class RoleBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class RolePublic(RoleBase):
    id: int


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass
