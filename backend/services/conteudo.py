from typing import Annotated

from fastapi import Depends

from exceptions import NotFoundException
from models import Conteudo
from repositories import ConteudoRepositoryDep


class ConteudoService:
    def __init__(self, conteudo_repository: ConteudoRepositoryDep):
        self.conteudo_repository = conteudo_repository

    def get_conteudo(self, id: int) -> Conteudo:
        conteudo = self.conteudo_repository.get_conteudo(id)
        if not conteudo:
            raise NotFoundException("Conteúdo", id)

        return conteudo

    def get_conteudo_by_id_externo(self, id_externo: int, api_fonte: str) -> Conteudo | None:
        return self.conteudo_repository.get_conteudo_by_id_externo(id_externo, api_fonte)


ConteudoServiceDep = Annotated[ConteudoService, Depends(ConteudoService)]
