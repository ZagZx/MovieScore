from datetime import date, datetime

from models.conteudo import TipoConteudo
from .base import Base
from .conteudo import ImagensConteudo


class ConteudoAssistido(Base):
    id: int  # id externo
    tipo: TipoConteudo
    titulo: str
    titulo_original: str
    status: str
    imagens: ImagensConteudo
    data_lancamento: date | None = None


class AssistidoBase(Base):
    id: int
    data_adicao: datetime


class AssistidoRead(AssistidoBase):
    conteudo: ConteudoAssistido
