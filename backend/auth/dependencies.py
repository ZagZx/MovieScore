from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from typing import Annotated

from database import SessionDep
from models import Usuario
from .jwt import decode_access_token

# Esquema Bearer — extrai o token do header "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer()


def get_current_usuario(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: SessionDep,
) -> Usuario:
    """
    Dependência que valida o JWT e retorna o usuário autenticado.
    Levanta HTTP 401 em caso de token inválido/expirado ou usuário inexistente.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(credentials.credentials)
        usuario_id: int | None = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = session.get(Usuario, int(usuario_id))
    if usuario is None:
        raise credentials_exception

    return usuario


# Tipo anotado para injetar nas rotas protegidas
CurrentUsuarioDep = Annotated[Usuario, Depends(get_current_usuario)]
