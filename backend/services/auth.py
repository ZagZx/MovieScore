from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth import create_access_token, verify_password
from repositories import UsuarioRepositoryDep
from schemas.auth import LoginInput


class AuthService:
    def __init__(self, usuario_repository: UsuarioRepositoryDep):
        self.usuario_repository = usuario_repository

    def autenticar(self, dados: LoginInput) -> str:
        usuario = self.usuario_repository.get_usuario_by_email(dados.email)

        if not usuario or not verify_password(dados.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return create_access_token(data={"sub": str(usuario.id)})


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
