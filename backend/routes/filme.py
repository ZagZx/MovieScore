from fastapi import APIRouter, HTTPException, status

from constants import TMDB_API_URL, HEADERS_TMDB, PARAMS_TMDB
from utils import get_data, ExternalAPIException

filmes_router = APIRouter(prefix="/filmes", tags=["filmes"])


@filmes_router.get("")
def buscar_filmes(busca: str):
    url = TMDB_API_URL + "/search/movie"
    params = PARAMS_TMDB.copy()

    if busca:
        params["query"] = busca

    try:
        return get_data(url, params, HEADERS_TMDB)
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/em-alta")
def listar_filmes_em_alta():
    url = TMDB_API_URL + "/trending/movie/week"

    try:
        return get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/populares")
def listar_filmes_populares():
    url = TMDB_API_URL + "/movie/popular"

    try:
        return get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/{filme_id}")
def buscar_filme_id(filme_id: int):
    url = TMDB_API_URL + f"/movie/{filme_id}"

    try:
        data = get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    if data.get("success") is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado.",
        )

    return data

