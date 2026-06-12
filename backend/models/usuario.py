from typing import TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from utils import get_now_datetime_utc
from .base import Base
if TYPE_CHECKING:
    from .avaliacao import Avaliacao
    from .favorito import Favorito
    from .assistido import Assistido


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    foto_perfil_url: Mapped[Optional[str]] = mapped_column(String(255))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=get_now_datetime_utc,
        nullable=False
    )

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="usuario")
    assistidos: Mapped[list["Assistido"]] = relationship(back_populates="usuario")
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(back_populates="usuario")