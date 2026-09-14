from typing import Annotated

from fastapi import Depends

from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from services.schemas.serie import SerieListRead
from utils import get_data


class SerieRepository:
    def __init__(self):
        pass

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
