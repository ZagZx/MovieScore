from datetime import datetime

from .base import Base


class FavoritoCreate(Base):
    conteudo_id: int
    usuario_id: int


class FavoritoRead(Base):
    id: int
    conteudo_id: int
    usuario_id: int
    data_adicao: datetime


# class FavoritoUpdate(BaseModel):
# pass
