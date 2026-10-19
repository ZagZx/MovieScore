from fastapi import APIRouter

from schemas.auth import LoginInput, TokenResponse
from schemas.usuario import UsuarioRead
from services import AuthServiceDep
from auth import CurrentUsuarioDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
def login(dados: LoginInput, auth_service: AuthServiceDep):
    """
    Autentica o usuário com email e senha.
    Retorna um JWT de acesso em caso de sucesso.
    """
    token = auth_service.autenticar(dados)
    return TokenResponse(access_token=token)


@auth_router.get("/me", response_model=UsuarioRead)
def me(usuario_atual: CurrentUsuarioDep):
    """Retorna os dados do usuário autenticado."""
    return usuario_atual
