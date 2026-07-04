from fastapi import (
    APIRouter,
    status,
    UploadFile,
    Depends
)

from services import UsuarioServiceDep
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
)
from schemas.pagination import (
    CursorParams,
    CursorPage,
    CursorPaging
)

from auth import CurrentUsuarioDep   # <-- importado para proteger rotas


usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("", response_model=CursorPage[UsuarioRead])
def listar_usuarios(usuario_service: UsuarioServiceDep, pagingParams: CursorParams = Depends()):
    usuarios, paging = usuario_service.list_usuario(pagingParams.cursor, pagingParams.limit)

    return CursorPage(
        data = usuarios,
        paging = paging
    )


@usuario_router.get("/{id}", response_model=UsuarioRead)
def buscar_usuario(id: int, usuario_service: UsuarioServiceDep):
    return usuario_service.get_usuario(id)


@usuario_router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_json: UsuarioCreate, usuario_service: UsuarioServiceDep):
    return usuario_service.create_usuario(usuario_json)


# ── rotas que exigem autenticação ──────────────────────────────────────────────

@usuario_router.patch("/{id}", response_model=UsuarioRead)
def atualizar_usuario(
    id: int,
    usuario_form: UsuarioUpdate,
    usuario_service: UsuarioServiceDep,
    _: CurrentUsuarioDep,           # garante que o requisitante está autenticado
):
    return usuario_service.update_usuario(id, usuario_form)


@usuario_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    id: int,
    usuario_service: UsuarioServiceDep,
    _: CurrentUsuarioDep,
):
    usuario_service.delete_usuario(id)


@usuario_router.patch("/{id}/foto-perfil", response_model=UsuarioRead)
def atualizar_foto_perfil(
    id: int,
    foto_perfil: UploadFile,
    usuario_service: UsuarioServiceDep,
    _: CurrentUsuarioDep,
):
    return usuario_service.update_foto_perfil(id, foto_perfil)