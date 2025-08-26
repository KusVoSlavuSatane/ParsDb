from fastapi import APIRouter, HTTPException, status

from src.database.session import SessionDep

from .models import Analyze
from .service import analyze_temp

analyze = APIRouter()


@analyze.post("/")
def analyze_func(analyze_in: Analyze):
    try:
        a = analyze_temp(analyze_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    return a
