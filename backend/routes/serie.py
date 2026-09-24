from fastapi import APIRouter, Depends, status

from services import SerieServiceDep
from services.favorito import FavoritoServiceDep
from auth.dependencies import CurrentUsuarioDep
from schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from schemas.serie import SerieListRead, SerieRead
from schemas.favorito import SerieFavoritaRead


series_router = APIRouter(prefix="/series", tags=["Séries"])

@series_router.get("", response_model=TmdbPage[SerieListRead])
def buscar_series(
    busca: str,
    serie_service: SerieServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    series, total_pages, total_results = serie_service.search_series(
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
    series, total_pages, total_results = serie_service.list_series_em_alta(
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
    series, total_pages, total_results = serie_service.list_series_populares(
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
    return serie_service.get_serie_from_api_and_update_database(serie_id=serie_id)


@series_router.get("/{serie_id}/favoritos", response_model=list[SerieFavoritaRead])
def listar_series_favoritas(
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep
):
    return favorito_service.list_favoritos_serie(current_user.id)


@series_router.post("/{serie_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def adicionar_serie_aos_favoritos(
    serie_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep
):
    favorito_service.add_favorito_serie(serie_id, current_user.id)


@series_router.delete("/{serie_id}/favoritos", status_code=status.HTTP_204_NO_CONTENT)
def remover_serie_dos_favoritos(
    serie_id: int,
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep
):
    favorito_service.remove_favorito_serie(serie_id, current_user.id)
