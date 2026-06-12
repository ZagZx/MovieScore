from fastapi import FastAPI

from routes import (
    animes_router, 
    filmes_router, 
    usuario_router, 
    series_router
)


app = FastAPI()

app.include_router(usuario_router)
app.include_router(animes_router)
app.include_router(filmes_router)
app.include_router(series_router)