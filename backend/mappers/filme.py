from services.schemas.filme import FilmeListRead, FilmeRead, ImagensFilme
from constants import TMDB_IMAGE_STORAGE

class FilmeMapper:
    @staticmethod
    def _map_image(path: str | None, size: str) -> str | None:
        if not path:
            return None

        return f"{TMDB_IMAGE_STORAGE}/{size}{path}"

    @staticmethod
    def _map_genres(item: dict) -> list[dict]:
        genres: list[dict] = item.get("genres", [])

        return [
            {"id": int(genre["id"]), "nome": genre["name"]}
            for genre in genres
            if genre.get("id") is not None and genre.get("name")
        ]

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
            imagens=ImagensFilme(
                capa=FilmeMapper._map_image(item.get("poster_path"), "w500"),
                banner=FilmeMapper._map_image(item.get("backdrop_path"), "original"),
            ),
            generos=FilmeMapper._map_genres(item),
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
                imagens=ImagensFilme(
                    capa=FilmeMapper._map_image(item.get("poster_path"), "w500"),
                    banner=FilmeMapper._map_image(item.get("backdrop_path"), "original"),
                ),
                generos_ids=[int(genre_id) for genre_id in item.get("genre_ids", [])],
            )
            for item in items
        ]