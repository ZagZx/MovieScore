from models import Avaliacao, Conteudo, Usuario
from models.conteudo import TipoConteudo
from schemas.avaliacao import (
    AvaliacaoConteudoRead,
    AvaliacaoUsuarioRead,
    ConteudoAvaliacao,
    UsuarioAvaliacao,
)
from schemas.conteudo import ImagensConteudo

from .filme import FilmeMapper
from .serie import SerieMapper
from .usuario import UsuarioMapper


class AvaliacaoMapper:
    @staticmethod
    def map_conteudo(conteudo: Conteudo) -> ConteudoAvaliacao:
        """Monta o resumo do conteúdo a partir da tabela filme/serie/anime.

        Requer `conteudo.filme`, `conteudo.serie` e `conteudo.anime` já
        carregados (joinedload), senão cada item dispara queries extras.
        """
        match conteudo.tipo:
            case TipoConteudo.FILME:
                entidade, mapper = conteudo.filme, FilmeMapper
            case TipoConteudo.SERIE:
                entidade, mapper = conteudo.serie, SerieMapper
            case TipoConteudo.ANIME:
                # Kitsu já guarda URLs completas, sem prefixo de imagem
                entidade, mapper = conteudo.anime, None

        if mapper is None:
            capa, banner = entidade.capa, entidade.banner
        else:
            capa = mapper.map_image(entidade.capa, "w500")
            banner = mapper.map_image(entidade.banner, "original")

        return ConteudoAvaliacao(
            id=conteudo.id_externo,
            tipo=conteudo.tipo,
            titulo=entidade.titulo,
            imagens=ImagensConteudo(capa=capa, banner=banner),
        )

    @staticmethod
    def map_usuario(usuario: Usuario) -> UsuarioAvaliacao:
        return UsuarioAvaliacao(
            id=usuario.id,
            nome=usuario.nome,
            foto_perfil_url=UsuarioMapper.map_foto_perfil(usuario.foto_perfil_path),
        )

    @staticmethod
    def map_avaliacao_usuario(avaliacao: Avaliacao) -> AvaliacaoUsuarioRead:
        return AvaliacaoUsuarioRead(
            id=avaliacao.id,
            estrelas=float(avaliacao.estrelas),
            comentario=avaliacao.comentario,
            data_criacao=avaliacao.data_criacao,
            data_atualizacao=avaliacao.data_atualizacao,
            conteudo=AvaliacaoMapper.map_conteudo(avaliacao.conteudo),
        )

    @staticmethod
    def map_avaliacoes_usuario(
        avaliacoes: list[Avaliacao],
    ) -> list[AvaliacaoUsuarioRead]:
        return [AvaliacaoMapper.map_avaliacao_usuario(a) for a in avaliacoes]

    @staticmethod
    def map_avaliacao_conteudo(avaliacao: Avaliacao) -> AvaliacaoConteudoRead:
        return AvaliacaoConteudoRead(
            id=avaliacao.id,
            estrelas=float(avaliacao.estrelas),
            comentario=avaliacao.comentario,
            data_criacao=avaliacao.data_criacao,
            data_atualizacao=avaliacao.data_atualizacao,
            usuario=AvaliacaoMapper.map_usuario(avaliacao.usuario),
        )

    @staticmethod
    def map_avaliacoes_conteudo(
        avaliacoes: list[Avaliacao],
    ) -> list[AvaliacaoConteudoRead]:
        return [AvaliacaoMapper.map_avaliacao_conteudo(a) for a in avaliacoes]
