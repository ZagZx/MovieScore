from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base

if TYPE_CHECKING:
    from .conteudo import Conteudo
    from .usuario import Usuario


class Favorito(Base):
    """Representa um conteudo favorito de um usuario.

    Args:
        id: Identificador unico gerado automaticamente.
        conteudo_id: Identificador do conteudo favoritado.
        usuario_id: Identificador do usuario que favoritou o conteudo.
        data_adicao: Data e hora em que o favorito foi criado.
        conteudo: Relacionamento com o conteudo favoritado.
        usuario: Relacionamento com o usuario dono do favorito.
    """

    __tablename__ = "favorito"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    data_adicao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), insert_default=get_now_datetime_utc, nullable=False
    )

    conteudo: Mapped["Conteudo"] = relationship(back_populates="favoritos")
    usuario: Mapped["Usuario"] = relationship(back_populates="favoritos")
