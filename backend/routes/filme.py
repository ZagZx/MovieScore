from fastapi import APIRouter, HTTPException

from constants import TMDB_API_URL, HEADERS_TMDB, PARAMS_TMDB
from utils import get_data, ExternalAPIError

filmes_router = APIRouter(prefix="/filme", tags=["filme"])


@filmes_router.get("")
def buscar_filmes(busca: str):
    url = TMDB_API_URL + "/search/movie"
    params = PARAMS_TMDB.copy()

    if busca:
        params["query"] = busca

    try:
        return get_data(url, params, HEADERS_TMDB)
    except ExternalAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/em-alta")
def listar_filmes_em_alta():
    url = TMDB_API_URL + "/trending/movie/week"

    try:
        return get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    except ExternalAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)