from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from auth import CurrentUsuarioDep, create_access_token, create_refresh_token, decode_refresh_token, revoke_access_token, revoke_refresh_token
from schemas.auth import LoginInput, RefreshTokenInput, TokenResponse
from schemas.usuario import UsuarioRead
from services import AuthServiceDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])
optional_bearer_scheme = HTTPBearer(auto_error=False)


@auth_router.post("/login", response_model=TokenResponse)
def login(dados: LoginInput, auth_service: AuthServiceDep):
    """
    Autentica o usuário com email e senha.
    Retorna os JWTs de acesso e refresh em caso de sucesso.
    """
    tokens = auth_service.autenticar(dados)
    return TokenResponse(**tokens)


@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(dados: RefreshTokenInput):
    """Renova o access token usando um refresh token válido."""
    try:
        payload = decode_refresh_token(dados.refresh_token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        ) from exc

    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
        )

    access_token = create_access_token({"sub": str(usuario_id)})
    refresh_token = create_refresh_token({"sub": str(usuario_id)})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/logout")
def logout(
    dados: RefreshTokenInput,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(optional_bearer_scheme)] = None,
):
    """Revoga o refresh token e também invalida o access token atual, se fornecido."""
    try:
        revoke_refresh_token(dados.refresh_token)
    except JWTError:
        pass

    if credentials:
        try:
            revoke_access_token(credentials.credentials)
        except Exception:
            pass

    return {"detail": "Logout realizado com sucesso"}


@auth_router.get("/me", response_model=UsuarioRead)
def me(usuario_atual: CurrentUsuarioDep):
    """Retorna os dados do usuário autenticado."""
    return usuario_atual
