from abc import ABC

from constants import TMDB_IMAGE_STORAGE

class TmdbMapper:
    @staticmethod
    def map_image(path: str | None, size: str) -> str | None:
        if not path:
            return None

        return f"{TMDB_IMAGE_STORAGE}/{size}{path}"

    @staticmethod
    def unmap_image(url: str | None) -> str | None:
        if not url:
            return None

        return "/" + url.split("/")[-1]

    @staticmethod
    def map_genres(item: dict) -> list[dict]:
        genres: list[dict] = item.get("genres", [])

        return [
            {"id": int(genre["id"]), "nome": genre["name"]}
            for genre in genres
            if genre.get("id") is not None and genre.get("name")
        ]