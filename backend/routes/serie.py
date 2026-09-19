from fastapi import APIRouter, Depends, HTTPException, status

from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from services import SerieServiceDep
from schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from schemas.serie import SerieListRead, SerieRead
from utils import get_data, ExternalAPIException

series_router = APIRouter(prefix="/series", tags=["Séries"])


@series_router.get("", response_model=TmdbPage[SerieListRead])
def buscar_series(
    busca: str,
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.buscar_series(
        busca=busca,
        page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/em-alta", response_model=TmdbPage[SerieListRead])
def listar_series_em_alta(
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.listar_em_alta(
        page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/populares", response_model=TmdbPage[SerieListRead])
def listar_series_populares(
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.listar_populares(
        page=paginacao.page
    )

    return TmdbPage(
        data=series,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@series_router.get("/{serie_id}", response_model=SerieRead)
def buscar_serie(serie_id: int, serie_service: SerieServiceDep):
    return serie_service.buscar_serie(serie_id=serie_id)

