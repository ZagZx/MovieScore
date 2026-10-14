from pydantic import Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from models.conteudo import TipoConteudo
from schemas.conteudo import ImagensConteudo
from .base import Base


class AvaliacaoCreate(Base):
    estrelas: Decimal = Field(
        ge=0.5, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 0.5 e <= 5, step de 0.5
    comentario: Optional[str] = None

class AvaliacaoUpdate(Base):
    estrelas: Optional[Decimal] = Field(
        default=None, ge=0.5, le=5, multiple_of=0.5, decimal_places=1
    )  # >= 0.5 e <= 5, step de 0.5
    comentario: Optional[str] = None


class ConteudoAvaliacao(Base):
    id: int # id externo
    tipo: TipoConteudo
    titulo: str
    imagens: ImagensConteudo

class UsuarioAvaliacao(Base):
    id: int
    nome: str
    foto_perfil_url: Optional[str] = None

class AvaliacaoBase(Base):
    id: int
    estrelas: float
    comentario: Optional[str] = None
    data_criacao: datetime
    data_atualizacao: Optional[datetime]

class AvaliacaoConteudoRead(AvaliacaoBase):
    usuario: UsuarioAvaliacao

class AvaliacaoUsuarioRead(AvaliacaoBase):
    conteudo: ConteudoAvaliacao
