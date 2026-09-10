from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from database import SessionDep
from models import Conteudo
from models.conteudo import TipoConteudo


class ConteudoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_conteudo(self, id: int) -> Conteudo | None:
        return self.session.get(Conteudo, id)
    
    def get_conteudo_by_id_externo_and_api_fonte(self, id_externo: int, api_fonte: str) -> Conteudo | None:
        return self.session.scalar(
            select(Conteudo).where(
                Conteudo.id_externo == id_externo,
                Conteudo.api_fonte == api_fonte,
            )
        )

    def get_or_create_conteudo(
        self, id_externo: int, api_fonte: str, tipo: TipoConteudo
    ) -> Conteudo:
        conteudo = self.get_conteudo_by_id_externo_and_api_fonte(id_externo, api_fonte)
        if conteudo:
            return conteudo

        conteudo = Conteudo(id_externo=id_externo, api_fonte=api_fonte, tipo=tipo)
        try:
            self.session.add(conteudo)
            self.session.commit()
            self.session.refresh(conteudo)
            return conteudo
        except Exception:
            self.session.rollback()
            raise

ConteudoRepositoryDep = Annotated[
    ConteudoRepository, Depends(ConteudoRepository)
]
