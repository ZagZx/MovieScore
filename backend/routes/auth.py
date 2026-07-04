from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from database import SessionDep
from models import Usuario
from schemas.auth import LoginInput, TokenResponse
from schemas.usuario import UsuarioRead
from auth import create_access_token, CurrentUsuarioDep, verify_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
def login(dados: LoginInput, session: SessionDep):
    """
    Autentica o usuário com email e senha.
    Retorna um JWT de acesso em caso de sucesso.
    """
    usuario = session.scalar(
        select(Usuario).where(Usuario.email == dados.email)
    )

    if not usuario or not verify_password(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": str(usuario.id)})
    return TokenResponse(access_token=token)


@auth_router.get("/me", response_model=UsuarioRead)
def me(usuario_atual: CurrentUsuarioDep):
    """Retorna os dados do usuário autenticado."""
    return usuario_atual