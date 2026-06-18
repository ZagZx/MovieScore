from pydantic import (
    BaseModel
)
from datetime import datetime

from models.conteudo import TipoConteudo

# class ConteudoCreate(BaseModel):
#     pass

class ConteudoRead(BaseModel):
    id: int
    id_externo: int
    api_fonte: str
    tipo: TipoConteudo
    data_adicao: datetime

# class ConteudoUpdate(BaseModel):
#     pass