from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não encontrada no arquivo .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("JWT_EXPIRE_MINUTES", 30))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um JWT de acesso com os dados fornecidos."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodifica e valida um JWT.
    Lança JWTError se o token for inválido ou expirado.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
