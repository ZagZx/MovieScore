from datetime import datetime, date

from models.conteudo import TipoConteudo
from .base import Base
from .conteudo import ImagensConteudo


class ConteudoFavorito(Base):
    id: int  # id externo
    tipo: TipoConteudo
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None


class FavoritoBase(Base):
    id: int
    data_adicao: datetime


class FavoritoRead(FavoritoBase):
    conteudo: ConteudoFavorito
