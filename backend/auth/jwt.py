from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não encontrada no arquivo .env")

REFRESH_SECRET_KEY = getenv("JWT_REFRESH_SECRET_KEY") or SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("JWT_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("JWT_REFRESH_EXPIRE_DAYS", 7))

REVOKED_TOKENS: set[str] = set()


def _create_token(
    data: dict,
    secret_key: str,
    expires_delta: Optional[timedelta],
    token_type: str,
    default_expire_delta: timedelta,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else default_expire_delta
    )
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um JWT de acesso com os dados fornecidos."""
    return _create_token(
        data=data,
        secret_key=SECRET_KEY,
        expires_delta=expires_delta,
        token_type="access",
        default_expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um JWT de refresh com os dados fornecidos."""
    return _create_token(
        data=data,
        secret_key=REFRESH_SECRET_KEY,
        expires_delta=expires_delta,
        token_type="refresh",
        default_expire_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def _decode_token(token: str, expected_type: str, secret_key: str) -> dict:
    if token in REVOKED_TOKENS:
        raise JWTError("Token revogado")

    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    token_type = payload.get("type")
    if token_type != expected_type:
        raise JWTError(f"Tipo de token inválido: {token_type}")

    return payload


def decode_access_token(token: str) -> dict:
    """
    Decodifica e valida um JWT de acesso.
    Lança JWTError se o token for inválido, expirado ou revogado.
    """
    return _decode_token(token=token, expected_type="access", secret_key=SECRET_KEY)


def decode_refresh_token(token: str) -> dict:
    """
    Decodifica e valida um JWT de refresh.
    Lança JWTError se o token for inválido, expirado ou revogado.
    """
    return _decode_token(
        token=token, expected_type="refresh", secret_key=REFRESH_SECRET_KEY
    )


def revoke_access_token(token: str) -> None:
    """Revoga um token de acesso."""
    REVOKED_TOKENS.add(token)


def revoke_refresh_token(token: str) -> None:
    """Revoga um token de refresh."""
    decode_refresh_token(token)
    REVOKED_TOKENS.add(token)
