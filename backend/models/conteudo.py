import enum
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from constants import KITSU_API_URL, TMDB_API_URL
from utils import get_now_datetime_utc, get_enum_values
from .base import Base

if TYPE_CHECKING:
    from .avaliacao import Avaliacao
    from .favorito import Favorito
    from .assistido import Assistido
    from .filme import Filme
    from .serie import Serie


class TipoConteudo(enum.Enum):
    ANIME = "anime"
    FILME = "filme"
    SERIE = "serie"

class ApiFonte(enum.Enum):
    KITSU = "kitsu"
    TMDB = "tmdb"

URL_POR_FONTE = {
    ApiFonte.KITSU: KITSU_API_URL,
    ApiFonte.TMDB: TMDB_API_URL
}

class Conteudo(Base):
    __tablename__ = "conteudo"
    __table_args__ = (
        UniqueConstraint(
            "id_externo", "api_fonte", name="uq_conteudo_id_externo_api_fonte"
        ),
    )  # equivalente a UNIQUE (id_externo, api_fonte)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id_externo: Mapped[int] = mapped_column(BigInteger, nullable=False)
    api_fonte: Mapped[ApiFonte] = mapped_column(Enum(ApiFonte, values_callable=get_enum_values, name="api_fonte_enum"), nullable=False)
    tipo: Mapped[TipoConteudo] = mapped_column(Enum(TipoConteudo, values_callable=get_enum_values, name="tipo_conteudo_enum"), nullable=False)
    data_adicao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), insert_default=get_now_datetime_utc, nullable=False
    )

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="conteudo")
    assistidos: Mapped[list["Assistido"]] = relationship(back_populates="conteudo")
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(back_populates="conteudo")

    filme: Mapped["Filme" | None] = relationship(back_populates="conteudo")
    serie: Mapped["Serie" | None] = relationship(back_populates="conteudo")
