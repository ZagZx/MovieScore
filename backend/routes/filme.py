from fastapi import APIRouter, Depends

from schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from schemas.filme import FilmeListRead, FilmeRead
from services import FilmeServiceDep

filmes_router = APIRouter(prefix="/filmes", tags=["filmes"])


@filmes_router.get("", response_model=TmdbPage[FilmeListRead])
def buscar_filmes(
    busca: str,
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends()
):
    filmes, total_pages, total_results = filme_service.search_filmes(
        busca=busca,
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages
        )
    )


@filmes_router.get("/em-alta", response_model=TmdbPage[FilmeListRead])
def listar_filmes_em_alta(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_em_alta(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages
        )
    )


@filmes_router.get("/populares", response_model=TmdbPage[FilmeListRead])
def listar_filmes_populares(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_populares(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@filmes_router.get("/em-breve", response_model=TmdbPage[FilmeListRead])
def listar_filmes_em_breve(
    filme_service: FilmeServiceDep,
    paginacao: TmdbPaginationParams = Depends(),
):
    filmes, total_pages, total_results = filme_service.list_filmes_em_breve(
        page=paginacao.page,
    )

    return TmdbPage(
        data=filmes,
        pagination=TmdbPagination(
            page=paginacao.page,
            total_pages=total_pages,
            total_results=total_results,
            has_more=paginacao.page < total_pages,
        ),
    )


@filmes_router.get("/{filme_id}", response_model=FilmeRead)
def buscar_filme_id(filme_id: int, filme_service: FilmeServiceDep):
    return filme_service.get_filme(filme_id=filme_id)
