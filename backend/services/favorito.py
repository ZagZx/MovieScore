from typing import Annotated

from fastapi import Depends

from mappers.favorito import FavoritoMapper
from exceptions import ConflictException, NotFoundException
from models import Favorito
from repositories import FavoritoRepositoryDep
from schemas.favorito import SerieFavoritaRead
from .usuario import UsuarioService, UsuarioServiceDep
from .serie import SerieServiceDep
from .conteudo import ConteudoServiceDep


class FavoritoService:
    def __init__(
        self,
        favorito_repository: FavoritoRepositoryDep,
        usuario_service: UsuarioServiceDep,
        serie_service: SerieServiceDep,
        conteudo_service: ConteudoServiceDep,
    ):
        self.favorito_repository = favorito_repository
        self.usuario_service = usuario_service
        self.serie_service = serie_service
        self.conteudo_service = conteudo_service

    def get_favorito(self, favorito_id: int) -> Favorito:
        favorito = self.favorito_repository.get_favorito(favorito_id)
        if not favorito:
            raise NotFoundException("Favorito", favorito_id)
        return favorito

    def list_favoritos_serie(self, usuario_id: int) -> list[SerieFavoritaRead]:
        usuario = self.usuario_service.get_usuario(usuario_id)

        return FavoritoMapper.map_series(self.favorito_repository.list_series_favoritas(usuario))

    def add_favorito_serie(self, serie_id: int, usuario_id: int):
        # pega a serie do banco, se não houver, busca na API
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            result = self.serie_service.get_serie_from_api_and_update_database(serie_id)
        
            _, serie = result

        if self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(serie.conteudo_id, usuario.id):
            raise ConflictException("A série já está na lista de favoritos")

        self.favorito_repository.add_favorito_serie(serie, usuario)

    def remove_favorito_serie(self, serie_id: int, usuario_id: int):
        usuario = self.usuario_service.get_usuario(usuario_id)
        serie = self.serie_service.get_serie_from_db(serie_id)
        if not serie:
            raise NotFoundException("Série", serie_id)

        favorito = self.favorito_repository.get_favorito_by_conteudo_id_and_usuario_id(
            conteudo_id=serie.conteudo_id,
            usuario_id=usuario.id
        )

        # TODO
        # arrumar essa gambiarra
        if not favorito:
            exception = NotFoundException("Favorito", id=0)
            exception.message = "Série não encontrada nos favoritos"

            raise exception
        
        self.favorito_repository.delete_favorito(favorito)


FavoritoServiceDep = Annotated[FavoritoService, Depends(FavoritoService)]
