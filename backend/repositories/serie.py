from typing import Annotated

from fastapi import Depends

from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from schemas.serie import SerieListRead, SerieRead
from utils import get_data


class SerieRepository:
    def __init__(self):
        pass

    def buscar_serie(self, serie_id: int) -> SerieRead | None:
        data = get_data(
            f"{TMDB_API_URL}/tv/{serie_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )

        # A TMDB retorna 200 com {"success": false} para alguns IDs inválidos
        if data.get("success") is False:
            return None

        return SerieMapper.map_serie(data)

    def buscar_series(
        self, 
        busca: str, 
        page: int = 1
    ) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["query"] = busca
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/search/tv", params=params, headers=HEADERS_TMDB
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results

    def listar_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/trending/tv/week",
            params=params,
            headers=HEADERS_TMDB,
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results

    def listar_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/tv/popular",
            params=params,
            headers=HEADERS_TMDB,
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results


SerieRepositoryDep = Annotated[SerieRepository, Depends(SerieRepository)]
