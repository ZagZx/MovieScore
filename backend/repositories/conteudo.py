from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from database import SessionDep
from models import Conteudo


class ConteudoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_conteudo(self, id: int) -> Conteudo | None:
        return self.session.get(Conteudo, id)

    def get_conteudo_by_id_externo(self, id_externo: int, api_fonte: str) -> Conteudo | None:
        return self.session.scalar(
            select(Conteudo).where(
                Conteudo.id_externo == id_externo,
                Conteudo.api_fonte == api_fonte,
            )
        )


ConteudoRepositoryDep = Annotated[
    ConteudoRepository, Depends(ConteudoRepository)
]
