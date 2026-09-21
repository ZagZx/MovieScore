from schemas.filme import FilmeListRead, FilmeRead
from schemas.conteudo import ImagensConteudo
from constants import TMDB_IMAGE_STORAGE

from .tmdb import TmdbMapper

class FilmeMapper(TmdbMapper):
    @staticmethod
    def map_filme(item: dict) -> FilmeRead:
        return FilmeRead(
            id=int(item["id"]),
            titulo=item.get("title") or "",
            titulo_original=item.get("original_title") or "",
            idioma_original=item.get("original_language") or "",
            descricao=item.get("overview"),
            status=item.get("status") or "",
            data_lancamento=item.get("release_date") or None,
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
                status=item.get("status") or "",
                data_lancamento=item.get("release_date") or None,
                imagens=ImagensConteudo(
                    capa=FilmeMapper.map_image(item.get("poster_path"), "w500"),
                    banner=FilmeMapper.map_image(item.get("backdrop_path"), "original"),
                ),
                generos_ids=[int(genre_id) for genre_id in item.get("genre_ids", [])],
            )
            for item in items
        ]

