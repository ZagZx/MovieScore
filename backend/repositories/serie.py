from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from utils import get_data
from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from schemas.serie import SerieListRead, SerieRead
from models.serie import Serie
from models.conteudo import ApiFonte, TipoConteudo
from database import SessionDep
from repositories.conteudo import ConteudoRepositoryDep


class SerieRepository:
    def __init__(self, session: SessionDep, conteudo_repository: ConteudoRepositoryDep):
        self.session = session
        self.conteudo_repository = conteudo_repository

    def get_serie_from_api(self, serie_id: int) -> SerieRead | None:
        data = get_data(
            f"{TMDB_API_URL}/tv/{serie_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )

        # A TMDB retorna 200 com {"success": false} para alguns IDs inválidos
        if data.get("success") is False:
            return None

        return SerieMapper.map_serie(data)

    def get_serie_by_conteudo_id(self, conteudo_id: int) -> Serie | None:
        return self.session.scalar(
            select(Serie).where(
                Serie.conteudo_id == conteudo_id
            )
        )

    def create_serie(self, serie: Serie) -> Serie:
        try:
            self.session.add(serie)
            self.session.commit()
            self.session.refresh(serie)

            return serie
        except Exception:
            self.session.rollback()
            raise

    def update_serie(self, serie: Serie) -> Serie:
        try:
            self.session.commit()
            self.session.refresh(serie)

            return serie
        except Exception:
            self.session.rollback()
            raise

    def get_serie_and_update_database(self, serie_id: int) -> SerieRead | None:
        serie = self.get_serie_from_api(serie_id)
        if not serie:
            return

        conteudo = self.conteudo_repository.get_or_create_conteudo(
            id_externo=serie_id,
            api_fonte=ApiFonte.TMDB,
            tipo=TipoConteudo.SERIE
        )

        serie_db = self.get_serie_by_conteudo_id(conteudo.id)
        if serie_db:
            serie_db.titulo = serie.titulo
            serie_db.titulo_original = serie.titulo_original
            serie_db.status = serie.status
            serie_db.capa = serie.imagens.capa
            serie_db.banner = serie.imagens.banner
            serie_db.data_lancamento = serie.data_lancamento

            self.update_serie(serie_db)
        else:
            serie_db = Serie(
                conteudo_id = conteudo.id,
                titulo = serie.titulo,
                titulo_original = serie.titulo_original,
                status = serie.status,
                capa = serie.imagens.capa,
                banner = serie.imagens.banner,
                data_lancamento = serie.data_lancamento
            )
            self.create_serie(serie_db)
        return serie    

    def search_series(
        self, 
        busca: str, 
        page: int = 1
    ) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["query"] = busca
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/search/tv", params=params, headers=HEADERS_TMDB
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results

    def list_series_em_alta(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/trending/tv/week",
            params=params,
            headers=HEADERS_TMDB,
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results

    def list_series_populares(self, page: int = 1) -> tuple[list[SerieListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/tv/popular",
            params=params,
            headers=HEADERS_TMDB,
        )

        series = SerieMapper.map_series(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return series, total_pages, total_results


SerieRepositoryDep = Annotated[SerieRepository, Depends(SerieRepository)]
