from utils import str_to_date
from schemas.filme import FilmeListRead, FilmeRead
from schemas.conteudo import ImagensConteudo
from constants import TMDB_IMAGE_STORAGE

from .tmdb import TmdbMapper

class FilmeMapper(TmdbMapper):
    @staticmethod
    def map_status(status: str | None):
        STATUS_MAP = {
            "Rumored": "Em rumores",
            "Planned": "Planejado",
            "In Production": "Em produção",
            "Post Production": "Em pós-produção",
            "Released": "Lançado",
            "Canceled": "Cancelado",
        }
        if status not in STATUS_MAP.keys():
            print(f"Status desconhecido recebido do TMDB: {status}")

        return STATUS_MAP.get(status, "Desconhecido")

    @staticmethod
    def map_filme(item: dict) -> FilmeRead:
        return FilmeRead(
            id=int(item["id"]),
            titulo=item.get("title") or "",
            titulo_original=item.get("original_title") or "",
            idioma_original=item.get("original_language") or "",
            descricao=item.get("overview"),
            status=FilmeMapper.map_status(item.get("status")),
            data_lancamento=str_to_date(item.get("release_date")) ,
            duracao_minutos=item.get("runtime") or 0,
            imagens=ImagensConteudo(
                capa=FilmeMapper.map_image(item.get("poster_path"), "w500"),
                banner=FilmeMapper.map_image(item.get("backdrop_path"), "original"),
            ),
            generos=FilmeMapper.map_genres(item),
        )

    @staticmethod
    def map_filmes(items: list[dict]) -> list[FilmeListRead]:
        return [
            FilmeListRead(
                id=int(item["id"]),
                titulo=item.get("title") or "",
                titulo_original=item.get("original_title") or "",
                idioma_original=item.get("original_language") or "",
                descricao=item.get("overview"),
                # status=FilmeMapper.map_status(item.get("status")),
                data_lancamento=str_to_date(item.get("release_date")),
                imagens=ImagensConteudo(
                    capa=FilmeMapper.map_image(item.get("poster_path"), "w500"),
                    banner=FilmeMapper.map_image(item.get("backdrop_path"), "original"),
                ),
                generos_ids=[int(genre_id) for genre_id in item.get("genre_ids", [])],
            )
            for item in items
        ]

