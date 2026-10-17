from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from database import SessionDep
from models import Avaliacao, Usuario, Conteudo


class AvaliacaoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def list_avaliacoes_by_usuario(
        self, usuario: Usuario, last_id: int, limit: int
    ) -> tuple[list[Avaliacao], bool]:
        """Retorna uma página de avaliações de um usuário específico."""
        avaliacoes = self.session.scalars(
            select(Avaliacao)
            .where(Avaliacao.usuario_id == usuario.id, Avaliacao.id > last_id)
            .order_by(Avaliacao.id)
            .limit(limit + 1)
        ).all()
        has_more = len(avaliacoes) > limit
        return avaliacoes[:limit], has_more

    def list_avaliacoes_by_conteudo(
        self, conteudo: Conteudo, last_id: int, limit: int
    ) -> tuple[list[Avaliacao], bool]:
        """Retorna uma página de avaliações de um conteúdo específico."""
        avaliacoes = self.session.scalars(
            select(Avaliacao)
            .where(Avaliacao.conteudo_id == conteudo.id, Avaliacao.id > last_id)
            .order_by(Avaliacao.id)
            .limit(limit + 1)
        ).all()
        has_more = len(avaliacoes) > limit
        return avaliacoes[:limit], has_more

    def get_avaliacao_by_usuario_and_conteudo(
        self, usuario: Usuario, conteudo: Conteudo
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        return self.session.scalar(
            select(Avaliacao).where(
                Avaliacao.usuario_id == usuario.id,
                Avaliacao.conteudo_id == conteudo.id,
            )
        )

    def create_avaliacao(self, avaliacao: Avaliacao) -> Avaliacao:
        self.session.add(avaliacao)
        self.session.flush()
        return avaliacao

    def update_avaliacao(self, avaliacao: Avaliacao) -> Avaliacao:
        self.session.flush()
        return avaliacao

    def delete_avaliacao(self, avaliacao: Avaliacao):
        self.session.delete(avaliacao)
        self.session.flush()


AvaliacaoRepositoryDep = Annotated[AvaliacaoRepository, Depends(AvaliacaoRepository)]
