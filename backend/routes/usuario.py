from fastapi import APIRouter, status, UploadFile, Depends

from services import UsuarioServiceDep, AvaliacaoServiceDep, FavoritoServiceDep
from schemas.avaliacao import AvaliacaoUsuarioRead
from schemas.favorito import FavoritoRead
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
)
from models.conteudo import TipoConteudo
from schemas.pagination.cursor import (
    CursorMediaPaginationParams,
    CursorPaginationParams,
    CursorPage,
)
from auth.dependencies import CurrentUsuarioDep

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("", response_model=CursorPage[UsuarioRead])
def listar_usuarios(
    usuario_service: UsuarioServiceDep, pagingParams: CursorPaginationParams = Depends()
):
    usuarios, paging = usuario_service.list_usuarios(
        pagingParams.cursor, pagingParams.limit
    )

    return CursorPage(data=usuarios, pagination=paging)


@usuario_router.post(
    "", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED
)
def criar_usuario(usuario_json: UsuarioCreate, usuario_service: UsuarioServiceDep):
    return usuario_service.create_usuario(usuario_json)


@usuario_router.get("/avaliacoes", response_model=CursorPage[AvaliacaoUsuarioRead])
def listar_avaliacoes_do_usuario_logado(
    current_user: CurrentUsuarioDep,
    avaliacao_service: AvaliacaoServiceDep,
    paging_params: CursorMediaPaginationParams = Depends(),
):
    avaliacoes, paging = avaliacao_service.list_avaliacoes_usuario(
        current_user.id,
        paging_params.cursor,
        paging_params.limit,
        paging_params.ordenacao,
    )
    return CursorPage(data=avaliacoes, pagination=paging)


@usuario_router.get("/favoritos", response_model=CursorPage[FavoritoRead])
def listar_favoritos_do_usuario_logado(
    current_user: CurrentUsuarioDep,
    favorito_service: FavoritoServiceDep,
    tipo: TipoConteudo | None = None,
    paging_params: CursorMediaPaginationParams = Depends(),
):

    items, pagination = favorito_service.list_conteudos_favoritos(
        current_user.id,
        paging_params.ordenacao,
        tipo,
        paging_params.cursor,
        paging_params.limit,
    )
    return CursorPage(data=items, pagination=pagination)


@usuario_router.patch("", response_model=UsuarioRead)
def atualizar_usuario(
    current_user: CurrentUsuarioDep,
    usuario_form: UsuarioUpdate,
    usuario_service: UsuarioServiceDep,
):
    id = current_user.id
    return usuario_service.update_usuario(id, usuario_form)


@usuario_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    current_user: CurrentUsuarioDep,
    usuario_service: UsuarioServiceDep,
):
    id = current_user.id
    usuario_service.delete_usuario(id)


@usuario_router.patch("/foto-perfil", response_model=UsuarioRead)
def atualizar_foto_perfil(
    current_user: CurrentUsuarioDep,
    foto_perfil: UploadFile,
    usuario_service: UsuarioServiceDep,
):
    id = current_user.id
    return usuario_service.update_foto_perfil(id, foto_perfil)


@usuario_router.get("/{id}", response_model=UsuarioRead)
def buscar_usuario(id: int, usuario_service: UsuarioServiceDep):
    return usuario_service.get_usuario(id)
