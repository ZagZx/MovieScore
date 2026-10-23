from typing import Annotated

from fastapi import Depends
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import contains_eager

from database import SessionDep
from models import Anime, Assistido, Usuario, Conteudo, Filme, Serie
from models.conteudo import TipoConteudo
from schemas.pagination.cursor import OrdenacaoCursor


class AssistidoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_assistido(self, id: int) -> Assistido | None:
        return self.session.get(Assistido, id)

    def get_assistido_by_conteudo_id_and_usuario_id(
        self, conteudo_id: int, usuario_id: int
    ) -> Assistido | None:
        return self.session.scalar(
            select(Assistido).where(
                Assistido.conteudo_id == conteudo_id,
                Assistido.usuario_id == usuario_id,
            )
        )

    def get_assistidos_usuario(self, usuario: Usuario) -> list[Assistido]:
        return self.session.scalars(
            select(Assistido).where(Assistido.usuario == usuario)
        )

    def list_conteudos_assistidos(
        self,
        usuario: Usuario,
        ordenacao: OrdenacaoCursor,
        tipo: TipoConteudo | None,
        last_id: int,
        limit: int,
    ) -> tuple[list[tuple[Filme | None, Serie | None, Anime | None, Assistido]], bool]:
        query = (
            select(Filme, Serie, Anime, Assistido)
            .select_from(Assistido)
            .join(Conteudo, Conteudo.id == Assistido.conteudo_id)
            .outerjoin(Filme, Filme.conteudo_id == Conteudo.id)
            .outerjoin(Serie, Serie.conteudo_id == Conteudo.id)
            .outerjoin(Anime, Anime.conteudo_id == Conteudo.id)
            .options(
                contains_eager(Filme.conteudo),
                contains_eager(Serie.conteudo),
                contains_eager(Anime.conteudo),
            )
            .where(Assistido.usuario_id == usuario.id)
        )
        if tipo:
            query = query.where(Conteudo.tipo == tipo)

        cursor_date = self.session.scalar(
            select(Assistido.data_adicao).where(
                Assistido.id == last_id, Assistido.usuario_id == usuario.id
            )
        )
        if cursor_date:
            if ordenacao is OrdenacaoCursor.RECENTES:
                query = query.where(
                    or_(
                        Assistido.data_adicao < cursor_date,
                        and_(
                            Assistido.data_adicao == cursor_date,
                            Assistido.id < last_id,
                        ),
                    )
                )
            else:
                query = query.where(
                    or_(
                        Assistido.data_adicao > cursor_date,
                        and_(
                            Assistido.data_adicao == cursor_date,
                            Assistido.id > last_id,
                        ),
                    )
                )

        order = (
            (Assistido.data_adicao.desc(), Assistido.id.desc())
            if ordenacao is OrdenacaoCursor.RECENTES
            else (Assistido.data_adicao.asc(), Assistido.id.asc())
        )
        items = self.session.execute(query.order_by(*order).limit(limit + 1)).all()
        has_more = len(items) > limit
        return items[:limit], has_more

    def add_assistido_serie(self, serie: Serie, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=serie.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def add_assistido_filme(self, filme: Filme, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=filme.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def add_assistido_anime(self, anime: Anime, usuario: Usuario) -> Assistido:
        assistido = Assistido(
            conteudo=anime.conteudo,
            usuario=usuario,
        )
        return self.create_assistido(assistido)

    def create_assistido(self, assistido: Assistido) -> Assistido:
        self.session.add(assistido)
        self.session.flush()
        return assistido

    def delete_assistido(self, assistido: Assistido):
        self.session.delete(assistido)
        self.session.flush()


AssistidoRepositoryDep = Annotated[AssistidoRepository, Depends(AssistidoRepository)]
