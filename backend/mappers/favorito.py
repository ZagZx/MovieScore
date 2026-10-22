from schemas.conteudo import ImagensConteudo
from schemas.favorito import ConteudoFavorito, FavoritoRead
from models.conteudo import TipoConteudo
from models import (
    Anime,
    Favorito,
    Filme,
    Serie,
)
from .filme import FilmeMapper
from .serie import SerieMapper


class FavoritoMapper:
    @staticmethod
    def map_serie(serie: Serie, favorito: Favorito) -> FavoritoRead:
        return FavoritoRead(
            id=favorito.id,
            data_adicao=favorito.data_adicao,
            conteudo=ConteudoFavorito(
                id=serie.conteudo.id_externo,
                tipo=TipoConteudo.SERIE,
                titulo=serie.titulo,
                titulo_original=serie.titulo_original,
                status=serie.status,
                imagens=ImagensConteudo(
                    capa=SerieMapper.map_image(serie.capa, "w500"),
                    banner=SerieMapper.map_image(serie.banner, "original"),
                ),
                data_lancamento=serie.data_lancamento,
            ),
        )

    @staticmethod
    def map_series(items: list[tuple[Serie, Favorito]]) -> list[FavoritoRead]:
        return [FavoritoMapper.map_serie(serie, favorito) for serie, favorito in items]

    @staticmethod
    def map_filme(filme: Filme, favorito: Favorito) -> FavoritoRead:
        return FavoritoRead(
            id=favorito.id,
            conteudo=ConteudoFavorito(
                id=filme.conteudo.id_externo,
                tipo=TipoConteudo.FILME,
                titulo=filme.titulo,
                titulo_original=filme.titulo_original,
                status=filme.status,
                imagens=ImagensConteudo(
                    capa=FilmeMapper.map_image(filme.capa, "w500"),
                    banner=FilmeMapper.map_image(filme.banner, "original"),
                ),
                data_lancamento=filme.data_lancamento,
            ),
            data_adicao=favorito.data_adicao,
        )

    @staticmethod
    def map_filmes(items: list[tuple[Filme, Favorito]]) -> list[FavoritoRead]:
        return [FavoritoMapper.map_filme(filme, favorito) for filme, favorito in items]

    @staticmethod
    def map_anime(anime: Anime, favorito: Favorito) -> FavoritoRead:
        # Kitsu já retorna URLs completas, sem prefixo de imagem do TMDB
        return FavoritoRead(
            id=favorito.id,
            conteudo=ConteudoFavorito(
                id=anime.conteudo.id_externo,
                tipo=TipoConteudo.ANIME,
                titulo=anime.titulo,
                titulo_original=anime.titulo_original,
                status=anime.status,
                imagens=ImagensConteudo(
                    capa=anime.capa,
                    banner=anime.banner,
                ),
                data_lancamento=anime.data_lancamento,
            ),
            data_adicao=favorito.data_adicao,
        )

    @staticmethod
    def map_animes(items: list[tuple[Anime, Favorito]]) -> list[FavoritoRead]:
        return [FavoritoMapper.map_anime(anime, favorito) for anime, favorito in items]

    @staticmethod
    def map_conteudo(
        conteudo: Filme | Serie | Anime, favorito: Favorito
    ) -> FavoritoRead:
        if type(conteudo) is Filme:
            return FavoritoMapper.map_filme(conteudo, favorito)
        elif type(conteudo) is Serie:
            return FavoritoMapper.map_serie(conteudo, favorito)
        elif type(conteudo) is Anime:
            return FavoritoMapper.map_anime(conteudo, favorito)

    @staticmethod
    def map_conteudos(
        items: list[tuple[Filme, Serie, Anime, Favorito]],
    ) -> list[FavoritoRead]:
        conteudos_favoritos: list[FavoritoRead] = []
        for row in items:
            for i in range(0, len(row) - 1):
                if row[i] is not None:
                    conteudo: Filme | Serie | Anime = row[i]
                    break
            favorito: Favorito = row[-1]
            conteudos_favoritos.append(FavoritoMapper.map_conteudo(conteudo, favorito))
        return conteudos_favoritos
