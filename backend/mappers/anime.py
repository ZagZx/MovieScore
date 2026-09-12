from services.schemas.anime import StatusAnime, AnimeRead, ImagensAnime

class AnimeMapper:
    STATUS_MAP = {
        "current": StatusAnime.ANDAMENTO,
        "finished": StatusAnime.FINALIZADO,
        "tba": StatusAnime.A_SER_ANUNCIADO,
        "unreleased": StatusAnime.NAO_LANCADO,
        "upcoming": StatusAnime.POR_VIR,
    }

    @staticmethod
    def _map_genres(item: dict, included: list[dict]) -> list[dict]:
        relationships = item.get("relationships", {})
        genre_data = relationships.get("genres", {}).get("data", [])

        included_by_id = {
            resource["id"]: resource
            for resource in included
            if resource.get("type") == "genres"
        }

        return [
            {
                "id": int(genre["id"]),
                "nome": included_by_id[genre["id"]]["attributes"]["name"],
            }
            for genre in genre_data
            if genre["id"] in included_by_id
        ]
    
    @staticmethod
    def _map_categories(item: dict, included: list[dict]) -> list[dict]:
        relationships = item.get("relationships", {})
        category_data = relationships.get("categories", {}).get("data", [])

        included_by_id = {
            resource["id"]: resource
            for resource in included
            if resource.get("type") == "categories"
        }

        return [
            {
                "id": int(category["id"]),
                "nome": included_by_id[category["id"]]["attributes"]["title"],
            }
            for category in category_data
            if category["id"] in included_by_id
        ]

    @staticmethod
    def map_anime(item: dict, included: list[dict]) -> AnimeRead:
        attributes: dict = item["attributes"]

        poster_image = attributes.get("posterImage") or {}
        cover_image = attributes.get("coverImage") or {}

        return AnimeRead(
            id=int(item["id"]),
            titulos=attributes.get("titles") or {},
            titulo_canonico=attributes.get("canonicalTitle") or "",
            descricao=attributes.get("description"),
            status=AnimeMapper.STATUS_MAP[attributes["status"]],
            data_inicio=attributes.get("startDate"),
            data_fim=attributes.get("endDate"),
            quantidade_episodios=attributes.get("episodeCount"),
            duracao_episodios=attributes.get("episodeLength"),
            imagens=ImagensAnime(
                capa=poster_image.get("original"),
                banner=cover_image.get("original"),
            ),
            generos=AnimeMapper._map_genres(item, included),
            categorias=AnimeMapper._map_categories(item, included),
        )

    @staticmethod
    def map_animes(items: list[dict], included: list[dict]) -> list[AnimeRead]:
        return [
            AnimeMapper.map_anime(item, included)
            for item in items
        ]