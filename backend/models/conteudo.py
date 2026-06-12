import enum
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, String, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base
if TYPE_CHECKING:
    from .avaliacao import Avaliacao
    from .favorito import Favorito
    from .assistido import Assistido


class TipoConteudo(enum.Enum):
    ANIME = "Anime"
    FILME = "Filme"
    SERIE = "Série"

class Conteudo(Base):
    __tablename__ = "conteudo"
    __table_args__ = (
        UniqueConstraint("id_externo", "api_fonte", name="uq_conteudo_id_externo_api_fonte"),
    ) # equivalente a UNIQUE (id_externo, api_fonte)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id_externo: Mapped[int] = mapped_column(BigInteger, nullable=False)
    api_fonte: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoConteudo] = mapped_column(Enum(TipoConteudo), nullable=False)
    data_adicao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=get_now_datetime_utc,
        nullable=False
    )

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="conteudo")
    assistidos: Mapped[list["Assistido"]] = relationship(back_populates="conteudo")
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(back_populates="conteudo")