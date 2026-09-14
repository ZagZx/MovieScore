from fastapi import APIRouter, Depends, HTTPException, status

from utils import get_data, ExternalAPIException
from constants import TMDB_API_URL, HEADERS_TMDB, PARAMS_TMDB
from services.schemas.pagination.tmdb import TmdbPage, TmdbPagination, TmdbPaginationParams
from services.schemas.filme import FilmeListRead
from mappers.filme import FilmeMapper

filmes_router = APIRouter(prefix="/filmes", tags=["filmes"])


@filmes_router.get("", response_model=TmdbPage[FilmeListRead])
def buscar_filmes(
    busca: str,
    paginacao: TmdbPaginationParams = Depends()
):
    url = TMDB_API_URL + "/search/movie"

    params = PARAMS_TMDB.copy()
    params["query"] = busca
    params["page"] = paginacao.page

    try:
        data = get_data(url, params, HEADERS_TMDB)

        items = data.get("results", [])
        filmes = FilmeMapper.map_filmes(items)

        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return TmdbPage(
            data=filmes,
            pagination=TmdbPagination(
                page=paginacao.page,
                total_pages=total_pages,
                total_results=total_results,
                has_more=paginacao.page < total_pages
            )
        )
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/em-alta", response_model=TmdbPage[FilmeListRead])
def listar_filmes_em_alta(paginacao: TmdbPaginationParams = Depends()):
    url = TMDB_API_URL + "/trending/movie/week"

    params = PARAMS_TMDB.copy()
    
    try:
        data = get_data(url, params, HEADERS_TMDB)

        items = data.get("results", [])
        filmes = FilmeMapper.map_filmes(items)

        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return TmdbPage(
            data=filmes,
            pagination=TmdbPagination(
                page=paginacao.page,
                total_pages=total_pages,
                total_results=total_results,
                has_more=paginacao.page < total_pages
            )
        )
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/populares")
def listar_filmes_populares():
    url = TMDB_API_URL + "/movie/popular"

    try:
        return get_data(url, PARAMS_TMDB, HEADERS_TMDB)
    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@filmes_router.get("/em-breve")
def listar_filmes_em_breve():
    url = TMDB_API_URL + "/movie/upcoming"

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
