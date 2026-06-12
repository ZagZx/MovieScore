from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base
if TYPE_CHECKING:
    from .conteudo import Conteudo
    from .usuario import Usuario


class Assistido(Base):
    __tablename__ = "assistido"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    data_adicao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=get_now_datetime_utc,
        nullable=False
    )

    conteudo: Mapped["Conteudo" ] = relationship(back_populates="assistidos")
    usuario: Mapped["Usuario" ] = relationship(back_populates="assistidos")