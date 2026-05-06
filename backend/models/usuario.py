from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(min_length=3, max_length=50, unique=True)
    email: EmailStr = Field(max_length=150, unique=True)
    senha_hash: str