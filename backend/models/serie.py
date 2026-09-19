from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, DateTime, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date

from utils import get_now_datetime_utc
from .base import Base

if TYPE_CHECKING:
    from .conteudo import Conteudo


class Serie(Base):
    __tablename__ = "serie"

    # id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    conteudo_id: Mapped[int] = mapped_column(ForeignKey("conteudo.id"), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo_original: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    capa: Mapped[Optional[str]] = mapped_column(String(255))
    banner: Mapped[Optional[str]] = mapped_column(String(255))
    data_lancamento: Mapped[Optional[date]] = mapped_column(Date)
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), insert_default=get_now_datetime_utc, onupdate=get_now_datetime_utc, nullable=False)

    conteudo: Mapped["Conteudo"] = relationship(back_populates="serie")