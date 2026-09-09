from fastapi import APIRouter, status, UploadFile, Depends

from services import UsuarioServiceDep
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
)
from schemas.pagination import CursorParams, CursorPage
from auth.dependencies import CurrentUsuarioDep

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("", response_model=CursorPage[UsuarioRead])
def listar_usuarios(
    usuario_service: UsuarioServiceDep, pagingParams: CursorParams = Depends()
):
    usuarios, paging = usuario_service.list_usuarios(
        pagingParams.cursor, pagingParams.limit
    )

    return CursorPage(data=usuarios, paging=paging)


@usuario_router.get("/{id}", response_model=UsuarioRead)
def buscar_usuario(id: int, usuario_service: UsuarioServiceDep):
    return usuario_service.get_usuario(id)


@usuario_router.post(
    "", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED
)
def criar_usuario(usuario_json: UsuarioCreate, usuario_service: UsuarioServiceDep):
    return usuario_service.create_usuario(usuario_json)


# ── rotas que exigem autenticação ──────────────────────────────────────────────


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
