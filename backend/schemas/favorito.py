from pydantic import BaseModel
from datetime import datetime


class FavoritoCreate(BaseModel):
    conteudo_id: int
    usuario_id: int


class FavoritoRead(BaseModel):
    id: int
    conteudo_id: int
    usuario_id: int
    data_adicao: datetime


# class FavoritoUpdate(BaseModel):
# pass
