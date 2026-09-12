from typing import Annotated

from fastapi import Depends

from models import Avaliacao
from repositories import AvaliacaoRepositoryDep
from services.usuario import UsuarioServiceDep
from services.conteudo import ConteudoServiceDep

class AvaliacaoService:
    def __init__(self, avaliacao_repository: AvaliacaoRepositoryDep, usuario_service: UsuarioServiceDep, conteudo_service: ConteudoServiceDep):
        self.avaliacao_repository = avaliacao_repository
        self.usuario_service = usuario_service
        self.conteudo_service = conteudo_service

    def list_avaliacoes_usuario(self, usuario_id: int) -> list[Avaliacao]:
        """Retorna as avaliações do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        return self.avaliacao_repository.list_avaliacoes_by_usuario(usuario)

    def get_avaliacao_usuario_conteudo(
        self, usuario_id: int, conteudo_id: int
    ) -> Avaliacao | None:
        """Busca uma avaliação específica do usuário para um conteúdo."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        conteudo = self.conteudo_service.get_conteudo(conteudo_id)
        return self.avaliacao_repository.get_avaliacao_by_usuario_and_conteudo(
            usuario, 
            conteudo
        )


AvaliacaoServiceDep = Annotated[AvaliacaoService, Depends(AvaliacaoService)]
