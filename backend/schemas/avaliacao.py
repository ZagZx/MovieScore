from pydantic import (
    Field,
    BaseModel,
)
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AvaliacaoCreate(BaseModel):
    conteudo_id: int
    usuario_id: int
    estrelas: Decimal = Field(
        ge=1, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 1 e <= 5, step de 0.5
    comentario: Optional[str] = None


class AvaliacaoRead(BaseModel):
    id: int
    conteudo_id: int
    usuario_id: int
    estrelas: Decimal
    comentario: Optional[str]
    data_criacao: datetime
    data_atualizacao: Optional[datetime]


class AvaliacaoUpdate(BaseModel):
    estrelas: Optional[Decimal] = Field(
        default=None, ge=1, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 1 e <= 5, step de 0.5
    comentario: Optional[str] = None
