from typing import Annotated

from fastapi import Depends

from mappers.avaliacao import AvaliacaoMapper
from models.conteudo import TipoConteudo
from exceptions import ConflictException, NotFoundException
from models import Avaliacao
from repositories import AvaliacaoRepositoryDep
from schemas.avaliacao import AvaliacaoConteudoRead, AvaliacaoUsuarioRead, AvaliacaoCreate, AvaliacaoUpdate, AvaliacaoSerieRead, AvaliacaoFilmeRead, AvaliacaoAnimeRead, AvaliacaoBase
from services.usuario import UsuarioServiceDep
from services.conteudo import ConteudoServiceDep
from services.serie import SerieServiceDep
from services.filme import FilmeServiceDep
from services.anime import AnimeServiceDep


class AvaliacaoService:
    def __init__(
        self,
        avaliacao_repository: AvaliacaoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        conteudo_service: ConteudoServiceDep,
        serie_service: SerieServiceDep,
        filme_service: FilmeServiceDep,
        anime_service: AnimeServiceDep,
    ):
        self.avaliacao_repository = avaliacao_repository
        self.usuario_service = usuario_service
        self.conteudo_service = conteudo_service
        self.serie_service = serie_service
        self.filme_service = filme_service
        self.anime_service = anime_service

    def list_avaliacoes_usuario(self, usuario_id: int) -> list[AvaliacaoUsuarioRead]:
        """Retorna as avaliações do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        avaliacoes = self.avaliacao_repository.list_avaliacoes_by_usuario(usuario)
        return AvaliacaoMapper.map_avaliacoes_usuario(avaliacoes)

    def list_avaliacoes_conteudo(self, id_externo: int, tipo: TipoConteudo) -> list[AvaliacaoConteudoRead]:
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(id_externo, tipo)
        avaliacoes = self.avaliacao_repository.list_avaliacoes_by_conteudo(conteudo)
        return AvaliacaoMapper.map_avaliacoes_conteudo(avaliacoes)

    def list_avaliacoes_serie(self, serie_id: int) -> list[AvaliacaoConteudoRead]:
        """Retorna todas as avaliações de uma série específica."""
        return self.list_avaliacoes_conteudo(serie_id, tipo="serie")

    # --- Filme evaluations ---
    def list_avaliacoes_filme(self, filme_id: int) -> list[AvaliacaoConteudoRead]:
        return self.list_avaliacoes_conteudo(filme_id, tipo="filme")

    # --- Anime evaluations ---
    def list_avaliacoes_anime(self, anime_id: int) -> list[Avaliacao]:
        return self.list_avaliacoes_conteudo(anime_id, tipo="anime")

    def create_avaliacao_anime(
        self, anime_id: int, usuario_id: int, avaliacao_data: AvaliacaoCreate
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao_existente = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou este anime")

        avaliacao = Avaliacao(
            conteudo=anime.conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )

        avaliacao_criada = self.avaliacao_repository.create_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoAnimeRead

        return AvaliacaoAnimeRead(
            id=avaliacao_criada.id,
            usuario_id=avaliacao_criada.usuario_id,
            estrelas=avaliacao_criada.estrelas,
            comentario=avaliacao_criada.comentario,
            data_criacao=avaliacao_criada.data_criacao,
            data_atualizacao=avaliacao_criada.data_atualizacao,
            anime_id=anime_id,
        )

    def update_avaliacao_anime(
        self, anime_id: int, usuario_id: int, avaliacao_data: AvaliacaoUpdate
    ) -> AvaliacaoAnimeRead:
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do anime não encontrada para o usuário atual")

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        avaliacao_atualizada = self.avaliacao_repository.update_avaliacao(avaliacao)

        from schemas.avaliacao import AvaliacaoAnimeRead

        return AvaliacaoAnimeRead(
            id=avaliacao_atualizada.id,
            usuario_id=avaliacao_atualizada.usuario_id,
            estrelas=avaliacao_atualizada.estrelas,
            comentario=avaliacao_atualizada.comentario,
            data_criacao=avaliacao_atualizada.data_criacao,
            data_atualizacao=avaliacao_atualizada.data_atualizacao,
            anime_id=anime_id,
        )

    def delete_avaliacao_anime(self, anime_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        anime = self.anime_service.get_anime_from_db(anime_id)
        if not anime:
            _, anime = self.anime_service.get_anime_from_api_and_update_database(anime_id)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            anime.conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do anime não encontrada para o usuário atual")

        self.avaliacao_repository.delete_avaliacao(avaliacao)

    def get_avaliacao_usuario_conteudo(
        self, usuario_id: int, conteudo_id: int
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo(conteudo_id)
        return self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )

    def create_avaliacao(
        self, avaliacao_data: AvaliacaoCreate, id_externo: int, usuario_id: int, tipo_conteudo: TipoConteudo, 
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(id_externo, tipo_conteudo)

        avaliacao_existente = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )
        if avaliacao_existente:
            raise ConflictException("Você já avaliou este conteúdo")

        avaliacao = Avaliacao(
            conteudo=conteudo,
            usuario=usuario,
            estrelas=avaliacao_data.estrelas,
            comentario=avaliacao_data.comentario,
        )

        return self.avaliacao_repository.create_avaliacao(avaliacao)

    def update_avaliacao(
        self, avaliacao_data: AvaliacaoUpdate, id_externo: int, usuario_id: int, tipo_conteudo: TipoConteudo
    ) -> Avaliacao:
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(id_externo, tipo_conteudo)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do conteúdo não encontrada para o usuário atual")

        if avaliacao_data.estrelas is not None:
            avaliacao.estrelas = avaliacao_data.estrelas
        if avaliacao_data.comentario is not None:
            avaliacao.comentario = avaliacao_data.comentario

        return self.avaliacao_repository.update_avaliacao(avaliacao)

    def delete_avaliacao(self, id_externo: int, usuario_id: int, tipo_conteudo: TipoConteudo):
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo_by_id_externo_and_tipo(id_externo, tipo_conteudo)

        avaliacao = self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario,
            conteudo,
        )
        if not avaliacao:
            raise NotFoundException("Avaliação do conteúdo não encontrada para o usuário atual")

        self.avaliacao_repository.delete_avaliacao(avaliacao)


AvaliacaoServiceDep = Annotated[AvaliacaoService, Depends(AvaliacaoService)]
