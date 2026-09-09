from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from database import SessionDep
from models import Favorito, Usuario, Conteudo


class FavoritoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_favorito(self, id: int) -> Favorito | None:
        return self.session.get(Favorito, id)

    def list_favoritos_by_usuario(self, usuario: Usuario) -> list[Favorito]:
        """Retorna todos os favoritos de um usuário específico."""
        return (
            self.session.scalars(
                select(Favorito)
                .where(Favorito.usuario_id == usuario.id)
                .order_by(Favorito.data_adicao.desc())
            )
            .all()
        )

    def get_favorito_by_usuario_and_conteudo(
        self, usuario: Usuario, conteudo: Conteudo
    ) -> Favorito | None:
        """Busca um favorito específico do usuário para um conteúdo."""
        return self.session.scalar(
            select(Favorito).where(
                Favorito.usuario_id == usuario.id,
                Favorito.conteudo_id == conteudo.id,
            )
        )

    def create_favorito(self, favorito: Favorito) -> Favorito:
        try:
            self.session.add(favorito)
            self.session.commit()
            self.session.refresh(favorito)
            return favorito
        except Exception:
            self.session.rollback()
            raise

    def delete_favorito(self, favorito: Favorito):
        try:
            self.session.delete(favorito)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise


FavoritoRepositoryDep = Annotated[
    FavoritoRepository, Depends(FavoritoRepository)
]
