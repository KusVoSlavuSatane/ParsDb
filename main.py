from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from src.analyze.routes import analyze
from src.database import create_db, engine
from src.field.routes import fields
from src.model.routes import models
from src.role.routes import roles
from src.user.routes import users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, dict]:  # noqa: ARG001
    print("The app is starting up!")

    create_db()

    yield  # FastAPI runs the application here

    print("The app is shutting down!")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(db, prefix="/db", tags=["Database"])
app.include_router(users, prefix="/users", tags=["Users"])
app.include_router(roles, prefix="/roles", tags=["Users"])
app.include_router(fields, prefix="/fields", tags=["Fields"])
app.include_router(models, prefix="/models", tags=["Models"])
app.include_router(analyze, prefix="/analyze", tags=["Analyze"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
