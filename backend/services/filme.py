from typing import Annotated

from fastapi import Depends

from exceptions import EntityNotFoundException
from repositories import FilmeRepositoryDep
from schemas.filme import FilmeListRead, FilmeRead


class FilmeService:
    def __init__(self, filme_repository: FilmeRepositoryDep):
        self.filme_repository = filme_repository

    def get_filme(self, filme_id: int) -> FilmeRead:
        filme = self.filme_repository.get_filme_and_update_database(filme_id)
        if not filme:
            raise EntityNotFoundException("Filme", filme_id)

        return filme

    def search_filmes(
        self, busca: str, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.search_filmes(busca=busca, page=page)

    def list_filmes_em_alta(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_em_alta(page=page)

    def list_filmes_populares(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_populares(page=page)

    def list_filmes_em_breve(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        return self.filme_repository.list_filmes_em_breve(page=page)


FilmeServiceDep = Annotated[FilmeService, Depends(FilmeService)]
