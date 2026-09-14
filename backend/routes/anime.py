from fastapi import APIRouter, Depends, HTTPException

from constants import KITSU_API_URL, HEADERS_KITSU
from utils import get_data, ExternalAPIException
from services.schemas.anime import AnimeRead
from services.schemas.pagination.kitsu import (
    KitsuPaginationParams,
    KitsuPage,
    KitsuPagination,
)
from mappers.anime import AnimeMapper

animes_router = APIRouter(prefix="/animes", tags=["animes"])


@animes_router.get("", response_model=KitsuPage[AnimeRead])
def buscar_animes(
    busca: str, 
    paginacao: KitsuPaginationParams = Depends()
):
    url = KITSU_API_URL + "/anime"
    params = paginacao.to_kitsu_query_params()
    params["filter[text]"] = busca
    params["include"] = "genres,categories"
    params["fields[genres]"] = "name"
    params["fields[categories]"] = "title"

    try:
        data = get_data(url, params, HEADERS_KITSU)

        items = data.get("data", [])
        included = data.get("included", [])
        animes = AnimeMapper.map_animes(items, included)

        meta: dict = data.get("meta", {})
        total_results = meta.get("count", 0)

        return KitsuPage(
            data=animes,
            pagination=KitsuPagination(
                limit=paginacao.limit,
                offset=paginacao.offset,
                total_results=total_results,
                has_more=paginacao.offset + paginacao.limit < total_results,
            ),
        )

    except ExternalAPIException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
