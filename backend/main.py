from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from routes import (
    animes_router, 
    filmes_router, 
    usuario_router, 
    series_router
)
from exceptions import (
    NotFoundException,
    ConflictException
)


app = FastAPI()


@app.exception_handler(Exception)
def generic_handler(request: Request, exc: Exception):
    print(exc)

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {"detail": "Erro interno"}
    )

@app.exception_handler(NotFoundException)
def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"detail": exc.message}
    )

@app.exception_handler(ConflictException)
def conflict_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"detail": exc.message}
    )

app.include_router(usuario_router)
app.include_router(animes_router)
app.include_router(filmes_router)
app.include_router(series_router)