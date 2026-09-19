from typing import Annotated

from fastapi import Depends

from repositories import SerieRepositoryDep
from schemas.serie import SerieListRead, SerieRead
from exceptions import NotFoundException


class SerieService:
    def __init__(self, serie_repository: SerieRepositoryDep):
        self.serie_repository = serie_repository

    def buscar_serie(self, serie_id: int) -> SerieRead:
        serie = self.serie_repository.buscar_serie(serie_id)
        if not serie:
            raise NotFoundException("Série", serie_id)

        return serie

    def buscar_series(self, busca: str, page: int=1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.buscar_series(busca=busca, page=page)

    def listar_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.listar_em_alta(page=page)

    def listar_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.listar_populares(page=page)


SerieServiceDep = Annotated[SerieService, Depends(SerieService)]
