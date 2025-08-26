from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URI = "sqlite:///./database.db"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


def get_session() -> Session:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
