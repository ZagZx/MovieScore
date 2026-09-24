from schemas.conteudo import ImagensConteudo
from schemas.favorito import SerieFavoritaRead
from models import (
    Favorito,
    Serie,
)
from .serie import SerieMapper


class FavoritoMapper:
    @staticmethod
    def map_serie(serie: Serie, favorito: Favorito) -> SerieFavoritaRead:
        return SerieFavoritaRead(
            id=serie.conteudo.id_externo,
            titulo=serie.titulo,
            titulo_original=serie.titulo_original,
            status=serie.status,
            imagens=ImagensConteudo(
                capa=SerieMapper.map_image(serie.capa, "w500"),
                banner=SerieMapper.map_image(serie.banner, "original")
            ),
            data_lancamento=serie.data_lancamento,
            data_adicao=favorito.data_adicao
        )

    @staticmethod
    def map_series(items: list[tuple[Serie, Favorito]]) -> list[SerieFavoritaRead]:
        return [
            FavoritoMapper.map_serie(serie, favorito)
            for serie, favorito in items
        ]