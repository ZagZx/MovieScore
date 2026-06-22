from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path

from constants import STORAGE
from routes import (
    animes_router,
    filmes_router,
    usuario_router,
    series_router,
    auth_router,
)
from exceptions import (
    NotFoundException,
    ConflictException,
    UnsupportedMediaTypeException,
)
from utils import ExternalAPIError


Path(STORAGE).mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.mount(f"/{STORAGE}", StaticFiles(directory=STORAGE), name="storage")


# ── handlers de exceção ───────────────────────────────────────────────────────

@app.exception_handler(Exception)
def generic_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno"},
    )


@app.exception_handler(NotFoundException)
def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(ConflictException)
def conflict_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


@app.exception_handler(UnsupportedMediaTypeException)
def unsupported_media_type_handler(request: Request, exc: UnsupportedMediaTypeException):
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={"detail": exc.message},
    )


@app.exception_handler(ExternalAPIError)
def external_api_error_handler(request: Request, exc: ExternalAPIError):
    """
    Captura ExternalAPIError não tratada dentro das rotas (segurança extra).
    Na prática as rotas já convertem para HTTPException, mas este handler
    garante que nenhum detalhe interno vaze para o cliente.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# ── routers ───────────────────────────────────────────────────────────────────

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(animes_router)
app.include_router(filmes_router)
app.include_router(series_router)