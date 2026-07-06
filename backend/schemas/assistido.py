from pydantic import BaseModel
from datetime import datetime


class AssistidoCreate(BaseModel):
    conteudo_id: int
    usuario_id: int


class AssistidoRead(BaseModel):
    id: int
    conteudo_id: int
    usuario_id: int
    data_adicao: datetime


# class AssistidoUpdate(BaseModel):
# pass
