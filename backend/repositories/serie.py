from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from utils import get_data
from constants import TMDB_API_URL, PARAMS_TMDB, HEADERS_TMDB
from mappers.serie import SerieMapper
from schemas.serie import SerieListRead, SerieRead
from models.serie import Serie
from models.conteudo import ApiFonte, Conteudo, TipoConteudo
from database import SessionDep


class SerieRepository:
    def __init__(self, session: SessionDep):
        self.session = session

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


    def get_serie_by_id_externo(self, id_externo: int) -> Serie | None:
        return self.session.scalar(
            select(Serie)
            .join(Serie.conteudo)
            .where(
                Conteudo.id_externo == id_externo,
                Conteudo.api_fonte == ApiFonte.TMDB,
                Conteudo.tipo == TipoConteudo.SERIE,
            )
        )

    def get_serie_by_conteudo_id(self, conteudo_id: int) -> Serie | None:
        return self.session.scalar(
            select(Serie).where(
                Serie.conteudo_id == conteudo_id
            )
        )

    def create_serie(self, serie: Serie) -> Serie:
        self.session.add(serie)
        self.session.flush()
        return serie

    def update_serie(self, serie: Serie) -> Serie:
        self.session.flush()
        return serie

    def create_or_update_serie(self, serie_from_api: SerieRead, conteudo: Conteudo) -> Serie:
        serie = self.get_serie_by_conteudo_id(conteudo.id)
        if serie:
            serie.titulo = serie_from_api.titulo
            serie.titulo_original = serie_from_api.titulo_original
            serie.status = serie_from_api.status
            serie.capa = SerieMapper.unmap_image(serie_from_api.imagens.capa)
            serie.banner = SerieMapper.unmap_image(serie_from_api.imagens.banner)
            serie.data_lancamento = serie_from_api.data_lancamento

            return self.update_serie(serie)
        serie_db = Serie(
            conteudo_id = conteudo.id,
            titulo = serie_from_api.titulo,
            titulo_original = serie_from_api.titulo_original,
            status = serie_from_api.status,
            capa = SerieMapper.unmap_image(serie_from_api.imagens.capa),
            banner = SerieMapper.unmap_image(serie_from_api.imagens.banner),
            data_lancamento = serie_from_api.data_lancamento
        )
        return self.create_serie(serie_db)

    def get_serie_and_update_database(self, serie_id: int, conteudo: Conteudo) -> SerieRead | None:
        serie = self.get_serie_from_api(serie_id)
        if not serie:
            return

        self.create_or_update_serie(serie, conteudo)
        
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
