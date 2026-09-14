from pydantic import Field

from .base import Base

class GeneroFilme(Base):
    id: int
    nome: str

class ImagensFilme(Base):
    capa: str | None = None #storage+poster_path
    banner: str | None = None #storage+backdrop_path

class FilmeListRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: str | None = None
    imagens: ImagensFilme
    generos_ids: list[int] = Field(default_factory=list)

class FilmeRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: str | None = None
    duracao_minutos: int = 0 # 0 é o padrão da api do TMDB
    imagens: ImagensFilme
    generos: list[GeneroFilme] = Field(default_factory=list)