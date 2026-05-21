from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoMidia(str, Enum):
    filme = "filme"
    serie = "serie"
    anime = "anime"

class Avaliacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key="usuario.id", index=True)

    # esse midia_id vai receber da API TMDB ou Kitsu 
    midia_id: str = Field(index=True)
    tipo: TipoMidia
    # não sei se vai ser de 0 a 10 ou 0 a 5 
    nota: float = Field(ge=0, le=10)
    comentario: Optional[str] = Field(default=None, max_length=1000)
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    atualizado_em: datetime = Field(default_factory=datetime.utcnow)

class AvaliacaoCreate(SQLModel):
    midia_id: str
    tipo: TipoMidia
    nota: float = Field(ge=0, le=10)
    comentario: Optional[str] = Field(default=None, max_length=1000)

class AvaliacaoUpdate(SQLModel):
    nota: Optional[float] = Field(default=None, ge=0, le=10)
    comentario: Optional[str] = Field(default=None, max_length=1000)

class AvaliacaoRead(SQLModel):
    id: int
    usuario_id: int
    midia_id: str
    tipo: TipoMidia
    nota: float
    comentario: Optional[str]
    criado_em: datetime
    atualizado_em: datetime