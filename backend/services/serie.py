from typing import Annotated

from fastapi import Depends

from repositories import SerieRepositoryDep
from schemas.serie import SerieListRead, SerieRead
from exceptions import NotFoundException


class SerieService:
    def __init__(self, serie_repository: SerieRepositoryDep):
        self.serie_repository = serie_repository

    def get_serie(self, serie_id: int) -> SerieRead:
        serie = self.serie_repository.get_serie_and_update_database(serie_id)
        if not serie:
            raise NotFoundException("Série", serie_id)

        return serie

    def search_series(self, busca: str, page: int=1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.search_series(busca=busca, page=page)

    def list_series_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.list_series_em_alta(page=page)

    def list_series_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.list_series_populares(page=page)


SerieServiceDep = Annotated[SerieService, Depends(SerieService)]
