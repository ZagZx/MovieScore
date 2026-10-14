from utils import str_to_date
from schemas.serie import SerieListRead, SerieRead, TemporadaSerie
from schemas.conteudo import ImagensConteudo
from constants import TMDB_IMAGE_STORAGE

from .tmdb import TmdbMapper

class SerieMapper(TmdbMapper):
    @staticmethod
    def map_status(status: str | None):
        STATUS_MAP = {
            "Returning Series": "Em exibição",
            "Planned": "Planejada",
            "In Production": "Em produção",
            "Ended": "Finalizada",
            "Canceled": "Cancelada",
            "Pilot": "Piloto",
        }
        if status not in STATUS_MAP.keys():
            print(f"Status desconhecido recebido do TMDB: {status}")

        return STATUS_MAP.get(status, "Desconhecido")

    @staticmethod
    def map_seasons(item: dict) -> list[TemporadaSerie]:
        seasons: list[dict] = item.get("seasons", [])

        return [
            TemporadaSerie(
                id=int(season["id"]),
                nome=season.get("name") or "",
                numero_temporada=season.get("season_number") or 0,
                quantidade_episodios=season.get("episode_count") or 0,
                descricao=season.get("overview"),
                data_lancamento=str_to_date(season.get("air_date")),
                capa=SerieMapper.map_image(season.get("poster_path"), "w500"),
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
            status=SerieMapper.map_status(item.get("status")),
            data_lancamento=str_to_date(item.get("first_air_date")),
            imagens=ImagensConteudo(
                capa=SerieMapper.map_image(item.get("poster_path"), "w500"),
                banner=SerieMapper.map_image(item.get("backdrop_path"), "original"),
            ),
            generos=SerieMapper.map_genres(item),
            duracao_episodios=[
                int(duration)
                for duration in item.get("episode_run_time", [])
            ],
            quantidade_episodios=item.get("number_of_episodes") or 0,
            quantidade_temporadas=item.get("number_of_seasons") or 0,
            temporadas=SerieMapper.map_seasons(item),
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
                # status=SerieMapper.map_status(item.get("status")),
                data_lancamento=str_to_date(item.get("first_air_date")),
                imagens=ImagensConteudo(
                    capa=SerieMapper.map_image(item.get("poster_path"), "w500"),
                    banner=SerieMapper.map_image(item.get("backdrop_path"), "original"),
                ),
                generos_ids=[int(genre_id) for genre_id in item.get("genre_ids", [])],
            )
            for item in items
        ]