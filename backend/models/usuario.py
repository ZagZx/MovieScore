from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional

class UsuarioBase(SQLModel):
    nome: str = Field(unique=True, min_length=2)
    email: EmailStr = Field(unique=True)


class UsuarioUpdate(SQLModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(default=None, min_length=8)

class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=8)

class UsuarioRead(UsuarioBase):
    id: int

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    senha_hash: str