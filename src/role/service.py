from sqlalchemy.orm import Session

from src.role.models import Role


def get_all(db: Session) -> list[Role]:
    return db.query(Role).all()
