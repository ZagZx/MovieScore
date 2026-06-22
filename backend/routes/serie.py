from fastapi import APIRouter, HTTPException, status

from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from utils import get_data, ExternalAPIError

series_router = APIRouter(prefix="/series", tags=["Séries"])


@series_router.get("")
def buscar_series(busca: str):
    params = PARAMS_TMDB.copy()
    if busca:
        params["query"] = busca

    try:
        data = get_data(f"{TMDB_API_URL}/search/tv", params=params, headers=HEADERS_TMDB)
        return data.get("results", [])
    except ExternalAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@series_router.get("/{serie_id}")
def buscar_serie(serie_id: int):
    try:
        data = get_data(
            f"{TMDB_API_URL}/tv/{serie_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )
    except ExternalAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    # A TMDB retorna 200 com {"success": false} para alguns IDs inválidos
    if data.get("success") is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Série não encontrada.",
        )

    return data