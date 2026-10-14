from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base

if TYPE_CHECKING:
    from .conteudo import Conteudo
    from .usuario import Usuario


class Assistido(Base):
    """Representa um conteudo marcado como assistido por um usuario.

    Args:
        id: Identificador unico gerado automaticamente.
        conteudo_id: Identificador do conteudo assistido.
        usuario_id: Identificador do usuario que assistiu ao conteudo.
        data_adicao: Data e hora em que o registro foi criado.
        conteudo: Relacionamento com o conteudo assistido.
        usuario: Relacionamento com o usuario que assistiu ao conteudo.
    """

    __tablename__ = "assistido"
    __table_args__ = (
        UniqueConstraint(
            "conteudo_id", "usuario_id", name="uq_conteudo_id_usuario_id"
        ),
    )  # equivalente a UNIQUE (conteudo_id, usuario_id)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    data_adicao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), insert_default=get_now_datetime_utc, nullable=False
    )

    conteudo: Mapped["Conteudo"] = relationship(back_populates="assistidos")
    usuario: Mapped["Usuario"] = relationship(back_populates="assistidos")
