from typing import Annotated

from fastapi import Depends

from exceptions import NotFoundException
from models.conteudo import ApiFonte, Conteudo, TipoConteudo
from repositories import ConteudoRepositoryDep


class ConteudoService:
    def __init__(self, conteudo_repository: ConteudoRepositoryDep):
        self.conteudo_repository = conteudo_repository

    def get_conteudo(self, id: int) -> Conteudo:
        conteudo = self.conteudo_repository.get_conteudo(id)
        if not conteudo:
            raise NotFoundException("Conteúdo", id)

        return conteudo

    def get_or_create_conteudo(self, id_externo: int, api_fonte: ApiFonte, tipo: TipoConteudo) -> Conteudo:
        return self.conteudo_repository.get_or_create_conteudo(
            id_externo=id_externo,
            api_fonte=api_fonte,
            tipo=tipo
        )


ConteudoServiceDep = Annotated[ConteudoService, Depends(ConteudoService)]
