from typing import TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped, relationship
from decimal import Decimal
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base

if TYPE_CHECKING:
    from .conteudo import Conteudo
    from .usuario import Usuario


class Avaliacao(Base):
    """Representa a avaliacao de um conteudo feita por um usuario.

    Args:
        id: Identificador unico gerado automaticamente.
        usuario_id: Identificador do usuario que fez a avaliacao.
        conteudo_id: Identificador do conteudo avaliado.
        estrelas: Nota atribuida ao conteudo.
        comentario: Comentario opcional sobre o conteudo.
        data_criacao: Data e hora em que a avaliacao foi criada.
        data_atualizacao: Data e hora da ultima atualizacao, quando houver.
        conteudo: Relacionamento com o conteudo avaliado.
        usuario: Relacionamento com o usuario que fez a avaliacao.
    """

    __tablename__ = "avaliacao"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), nullable=False)
    estrelas: Mapped[Decimal] = mapped_column(DECIMAL(2, 1), nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), insert_default=get_now_datetime_utc, nullable=False
    )
    data_atualizacao: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=get_now_datetime_utc
    )

    conteudo: Mapped["Conteudo"] = relationship(back_populates="avaliacoes")
    usuario: Mapped["Usuario"] = relationship(back_populates="avaliacoes")
