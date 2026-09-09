from typing import Annotated

from fastapi import Depends

from exceptions import ConflictException, NotFoundException
from models import Favorito
from repositories import FavoritoRepositoryDep
from services.conteudo import ConteudoServiceDep
from services.usuario import UsuarioServiceDep


class FavoritoService:
    def __init__(
        self,
        favorito_repository: FavoritoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        conteudo_service: ConteudoServiceDep,
    ):
        self.favorito_repository = favorito_repository
        self.usuario_service = usuario_service
        self.conteudo_service = conteudo_service

    def list_favoritos_usuario(self, usuario_id: int) -> list[Favorito]:
        """Retorna os favoritos do usuário autenticado."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        return self.favorito_repository.list_favoritos_by_usuario(usuario)

    def get_favorito_usuario_conteudo(
        self, usuario_id: int, conteudo_id: int
    ) -> Favorito | None:
        """Busca um favorito específico do usuário para um conteúdo."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        self.conteudo_service.get_conteudo(conteudo_id)
        return self.favorito_repository.get_favorito_by_usuario_and_conteudo(
            usuario, conteudo_id
        )

    def add_favorito_usuario(self, usuario_id: int, conteudo_id: int) -> Favorito:
        """Adiciona um conteúdo na lista de favoritos do usuário."""
        usuario = self.usuario_service.get_usuario(usuario_id)
        self.conteudo_service.get_conteudo(conteudo_id)

        if self.favorito_repository.get_favorito_by_usuario_and_conteudo(
            usuario, conteudo_id
        ):
            raise ConflictException("Este conteúdo já está nos favoritos do usuário")

        favorito = Favorito(usuario_id=usuario.id, conteudo_id=conteudo_id)
        return self.favorito_repository.create_favorito(favorito)

    def remove_favorito_usuario(self, usuario_id: int, conteudo_id: int):
        """Remove um conteúdo da lista de favoritos do usuário."""
        favorito = self.get_favorito_usuario_conteudo(usuario_id, conteudo_id)
        if not favorito:
            raise NotFoundException("Favorito", conteudo_id)

        self.favorito_repository.delete_favorito(favorito)


FavoritoServiceDep = Annotated[FavoritoService, Depends(FavoritoService)]
