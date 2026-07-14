from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database.session import check_database_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> JSONResponse:
    database_ok = check_database_connection()
    payload = {
        "status": "ok" if database_ok else "error",
        "database": "ok" if database_ok else "error",
    }
    status_code = 200 if database_ok else 503
    return JSONResponse(content=payload, status_code=status_code)
