from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from constants import HEADERS_TMDB, PARAMS_TMDB, TMDB_API_URL
from database import SessionDep
from mappers.filme import FilmeMapper
from models.conteudo import ApiFonte, TipoConteudo
from models.filme import Filme
from repositories.conteudo import ConteudoRepositoryDep
from schemas.filme import FilmeListRead, FilmeRead
from utils import get_data


class FilmeRepository:
    def __init__(self, session: SessionDep, conteudo_repository: ConteudoRepositoryDep):
        self.session = session
        self.conteudo_repository = conteudo_repository

    def get_filme_from_api(self, filme_id: int) -> FilmeRead | None:
        data = get_data(
            f"{TMDB_API_URL}/movie/{filme_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB,
        )

        if data.get("success") is False:
            return None

        return FilmeMapper.map_filme(data)

    def get_filme_by_conteudo_id(self, conteudo_id: int) -> Filme | None:
        return self.session.scalar(
            select(Filme).where(Filme.conteudo_id == conteudo_id)
        )

    def create_filme(self, filme: Filme) -> Filme:
        try:
            self.session.add(filme)
            self.session.commit()
            self.session.refresh(filme)
            return filme
        except Exception:
            self.session.rollback()
            raise

    def update_filme(self, filme: Filme) -> Filme:
        try:
            self.session.commit()
            self.session.refresh(filme)
            return filme
        except Exception:
            self.session.rollback()
            raise

    def get_filme_and_update_database(self, filme_id: int) -> FilmeRead | None:
        filme = self.get_filme_from_api(filme_id)
        if not filme:
            return None

        conteudo = self.conteudo_repository.get_or_create_conteudo(
            id_externo=filme_id,
            api_fonte=ApiFonte.TMDB,
            tipo=TipoConteudo.FILME,
        )

        filme_db = self.get_filme_by_conteudo_id(conteudo.id)
        if filme_db:
            filme_db.titulo = filme.titulo
            filme_db.titulo_original = filme.titulo_original
            filme_db.status = filme.status
            filme_db.capa = filme.imagens.capa
            filme_db.banner = filme.imagens.banner
            filme_db.data_lancamento = filme.data_lancamento
            self.update_filme(filme_db)
        else:
            filme_db = Filme(
                conteudo_id=conteudo.id,
                titulo=filme.titulo,
                titulo_original=filme.titulo_original,
                status=filme.status,
                capa=filme.imagens.capa,
                banner=filme.imagens.banner,
                data_lancamento=filme.data_lancamento,
            )
            self.create_filme(filme_db)

        return filme

    def search_filmes(
        self, busca: str, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["query"] = busca
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/search/movie",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_filmes_em_alta(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/trending/movie/week",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_filmes_populares(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/movie/popular",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results

    def list_filmes_em_breve(
        self, page: int = 1
    ) -> tuple[list[FilmeListRead], int, int]:
        params = PARAMS_TMDB.copy()
        params["page"] = page

        data = get_data(
            f"{TMDB_API_URL}/movie/upcoming",
            params=params,
            headers=HEADERS_TMDB,
        )

        filmes = FilmeMapper.map_filmes(data.get("results", []))
        total_pages = data.get("total_pages", 0)
        total_results = data.get("total_results", 0)

        return filmes, total_pages, total_results


FilmeRepositoryDep = Annotated[FilmeRepository, Depends(FilmeRepository)]
