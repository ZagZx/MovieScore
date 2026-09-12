from enum import Enum
from pydantic import Field

from .base import Base


class ImagensAnime(Base):
    capa: str | None = None #posterImage
    banner: str | None = None #coverImage

class GeneroAnime(Base):
    id: int
    nome: str

class CategoriaAnime(Base):
    id: int
    nome: str

class StatusAnime(str, Enum):
    ANDAMENTO = "Em andamento" #current
    FINALIZADO = "Finalizado" #finished
    A_SER_ANUNCIADO = "A ser anunciado" #tba
    NAO_LANCADO = "Não lançado" #unreleased
    POR_VIR = "Por vir" #upcoming


class AnimeRead(Base):
    id: int
    titulos: dict[str, str]
    titulo_canonico: str
    descricao: str | None = None
    status: StatusAnime
    data_inicio: str | None = None
    data_fim: str | None = None
    quantidade_episodios: int | None = None
    duracao_episodios: int | None = None
    imagens: ImagensAnime
    generos: list[GeneroAnime] = Field(default_factory=list)
    categorias: list[CategoriaAnime] = Field(default_factory=list)
