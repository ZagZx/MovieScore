from datetime import datetime

from models.conteudo import TipoConteudo
from .base import Base


class ConteudoCreate(Base):
    id_externo: int
    api_fonte: str
    tipo: TipoConteudo


class ConteudoRead(Base):
    id: int
    id_externo: int
    api_fonte: str
    tipo: TipoConteudo
    data_adicao: datetime


# class ConteudoUpdate(BaseModel):
#     pass
