from typing import Annotated

from fastapi import Depends

from repositories import SerieRepositoryDep
from services.schemas.serie import SerieListRead


class SerieService:
    def __init__(self, serie_repository: SerieRepositoryDep):
        self.serie_repository = serie_repository

    def listar_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.listar_em_alta(page=page)

    def listar_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        return self.serie_repository.listar_populares(page=page)


SerieServiceDep = Annotated[SerieService, Depends(SerieService)]
