from datetime import datetime

from .base import Base


class AssistidoCreate(Base):
    conteudo_id: int
    usuario_id: int


class AssistidoRead(Base):
    id: int
    conteudo_id: int
    usuario_id: int
    data_adicao: datetime


# class AssistidoUpdate(BaseModel):
# pass
