from pydantic import Field
from .base import Base


class ImagensField(Base):
    capa: str | None = None #posterImage
    banner: str | None = None #coverImage


class GeneroAnime(Base):
    id: int
    nome: str


class CategoriaAnime(Base):
    id: int
    nome: str


class AnimeRead(Base):
    id: int
    titulos: dict[str, str]
    titulo_canonico: str
    descricao: str | None = None
    imagens: ImagensField
    quantidade_episodios: int | None = None
    duracao_episodios: int | None = None
    generos: list[GeneroAnime] = Field(default_factory=list)
    categorias: list[CategoriaAnime] = Field(default_factory=list)