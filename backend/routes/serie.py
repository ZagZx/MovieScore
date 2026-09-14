from fastapi import APIRouter, Depends, HTTPException, status

from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from services.schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from services.schemas.serie import SerieListRead, SerieRead
from utils import get_data, ExternalAPIException

series_router = APIRouter(prefix="/series", tags=["Séries"])


@series_router.get("", response_model=TmdbPage[SerieListRead])
def buscar_series(
    busca: str,
    paginacao: TmdbPaginationParams = Depends(),
):
    params = PARAMS_TMDB.copy()
    params["query"] = busca
    params["page"] = paginacao.page

    try:
        data = get_data(
            f"{TMDB_API_URL}/search/tv", params=params, headers=HEADERS_TMDB
        )

        total_pages = data.get("total_pages", 0)
        return TmdbPage(
            data=SerieMapper.map_series(data.get("results", [])),
            pagination=TmdbPagination(
                page=paginacao.page,
                total_pages=total_pages,
                total_results=data.get("total_results", 0),
                has_more=paginacao.page < total_pages,
            ),
        )
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@series_router.get("/{serie_id}", response_model=SerieRead)
def buscar_serie(serie_id: int):
    try:
        data = get_data(
            f"{TMDB_API_URL}/tv/{serie_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    # A TMDB retorna 200 com {"success": false} para alguns IDs inválidos
    if data.get("success") is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Série não encontrada.",
        )

    return SerieMapper.map_serie(data)
