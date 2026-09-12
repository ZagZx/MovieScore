from pydantic import Field

from .base import Base

class GeneroSerie(Base):
    id: int
    nome: str

class ImagensSerie(Base):
    capa: str | None = None #storage+poster_path
    banner: str | None = None #storage+backdrop_path

class TemporadaSerie(Base):
    id: int
    data_lancamento: str | None = None
    quantidade_episodios: int = 0
    numero_temporada: int = 0
    descricao: str | None = None
    capa: str | None = None

class SerieListRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: str | None = None
    imagens: ImagensSerie
    generos_ids: list[int] = Field(default_factory=list)

class SerieRead(Base):
    id: int
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str | None = None
    status: str # TMDB não disponibiliza explicitamente a lista com todos os valores possíveis para Status
    data_lancamento: str | None = None
    imagens: ImagensSerie
    generos: list[GeneroSerie] = Field(default_factory=list)
    duracao_episodios: list[int]= Field(default_factory=list)
    quantidade_episodios: int = 0
    quantidade_temporadas: int = 0
    temporadas: list[TemporadaSerie] = Field(default_factory=list)