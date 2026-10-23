from schemas.conteudo import ImagensConteudo
from schemas.assistido import ConteudoAssistido, AssistidoRead
from models.conteudo import TipoConteudo
from models import (
    Anime,
    Assistido,
    Filme,
    Serie,
)
from .filme import FilmeMapper
from .serie import SerieMapper


class AssistidoMapper:
    @staticmethod
    def map_serie(serie: Serie, assistido: Assistido) -> AssistidoRead:
        return AssistidoRead(
            id=assistido.id,
            data_adicao=assistido.data_adicao,
            conteudo=ConteudoAssistido(
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
    def map_series(items: list[tuple[Serie, Assistido]]) -> list[AssistidoRead]:
        return [
            AssistidoMapper.map_serie(serie, assistido) for serie, assistido in items
        ]

    @staticmethod
    def map_filme(filme: Filme, assistido: Assistido) -> AssistidoRead:
        return AssistidoRead(
            id=assistido.id,
            conteudo=ConteudoAssistido(
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
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_filmes(items: list[tuple[Filme, Assistido]]) -> list[AssistidoRead]:
        return [
            AssistidoMapper.map_filme(filme, assistido) for filme, assistido in items
        ]

    @staticmethod
    def map_anime(anime: Anime, assistido: Assistido) -> AssistidoRead:
        # Kitsu já retorna URLs completas, sem prefixo de imagem do TMDB
        return AssistidoRead(
            id=assistido.id,
            conteudo=ConteudoAssistido(
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
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_animes(items: list[tuple[Anime, Assistido]]) -> list[AssistidoRead]:
        return [
            AssistidoMapper.map_anime(anime, assistido) for anime, assistido in items
        ]

    @staticmethod
    def map_conteudo(
        conteudo: Filme | Serie | Anime, assistido: Assistido
    ) -> AssistidoRead:
        if type(conteudo) is Filme:
            return AssistidoMapper.map_filme(conteudo, assistido)
        elif type(conteudo) is Serie:
            return AssistidoMapper.map_serie(conteudo, assistido)
        elif type(conteudo) is Anime:
            return AssistidoMapper.map_anime(conteudo, assistido)

    @staticmethod
    def map_conteudos(
        items: list[tuple[Filme, Serie, Anime, Assistido]],
    ) -> list[AssistidoRead]:
        conteudos_favoritos: list[AssistidoRead] = []
        for row in items:
            for i in range(0, len(row) - 1):
                if row[i] is not None:
                    conteudo: Filme | Serie | Anime = row[i]
                    break
            assistido: Assistido = row[-1]
            conteudos_favoritos.append(
                AssistidoMapper.map_conteudo(conteudo, assistido)
            )
        return conteudos_favoritos
