from services.schemas.serie import SerieListRead, SerieRead, ImagensSerie, TemporadaSerie
from constants import TMDB_IMAGE_STORAGE

class SerieMapper:
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
    def _map_seasons(item: dict) -> list[TemporadaSerie]:
        seasons: list[dict] = item.get("seasons", [])

        return [
            TemporadaSerie(
                id=int(season["id"]),
                data_lancamento=season.get("air_date") or None,
                quantidade_episodios=season.get("episode_count") or 0,
                numero_temporada=season.get("season_number") or 0,
                descricao=season.get("overview"),
                capa=SerieMapper._map_image(season.get("poster_path"), "w500"),
            )
            for season in seasons
            if season.get("id") is not None
        ]

    @staticmethod
    def map_serie(item: dict) -> SerieRead:
        return SerieRead(
            id=int(item["id"]),
            titulo=item.get("name") or "",
            titulo_original=item.get("original_name") or "",
            idioma_original=item.get("original_language") or "",
            descricao=item.get("overview"),
            status=item.get("status") or "",
            data_lancamento=item.get("first_air_date") or None,
            imagens=ImagensSerie(
                capa=SerieMapper._map_image(item.get("poster_path"), "w500"),
                banner=SerieMapper._map_image(item.get("backdrop_path"), "original"),
            ),
            generos=SerieMapper._map_genres(item),
            duracao_episodios=[
                int(duration)
                for duration in item.get("episode_run_time", [])
            ],
            quantidade_episodios=item.get("number_of_episodes") or 0,
            quantidade_temporadas=item.get("number_of_seasons") or 0,
            temporadas=SerieMapper._map_seasons(item),
        )

    @staticmethod
    def map_series(items: list[dict]) -> list[SerieListRead]:
        return [
            SerieListRead(
                id=int(item["id"]),
                titulo=item.get("name") or "",
                titulo_original=item.get("original_name") or "",
                idioma_original=item.get("original_language") or "",
                descricao=item.get("overview"),
                status=item.get("status") or "",
                data_lancamento=item.get("first_air_date") or None,
                imagens=ImagensSerie(
                    capa=SerieMapper._map_image(item.get("poster_path"), "w500"),
                    banner=SerieMapper._map_image(item.get("backdrop_path"), "original"),
                ),
                generos_ids=[int(genre_id) for genre_id in item.get("genre_ids", [])],
            )
            for item in items
        ]