from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from database import SessionDep
from models import Avaliacao, Usuario


class AvaliacaoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def list_avaliacoes_by_usuario(self, usuario: Usuario) -> list[Avaliacao]:
        """Retorna todas as avaliações de um usuário específico."""
        return (
            self.session.scalars(
                select(Avaliacao)
                .where(Avaliacao.usuario_id == usuario.id)
                .order_by(Avaliacao.data_criacao.desc())
            )
            .all()
        )

    def get_avaliacao_by_usuario_and_conteudo(
        self, usuario: Usuario, conteudo_id: int
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        return self.session.scalar(
            select(Avaliacao).where(
                Avaliacao.usuario_id == usuario.id,
                Avaliacao.conteudo_id == conteudo_id,
            )
        )


AvaliacaoRepositoryDep = Annotated[
    AvaliacaoRepository, Depends(AvaliacaoRepository)
]
