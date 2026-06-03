from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional


class UsuarioCreate(SQLModel):
    nome: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(max_length=150)
    senha: str = Field(min_length=8)

class UsuarioRead(SQLModel):
    id: int
    nome: str
    email: EmailStr

class UsuarioUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=150)
    senha: Optional[str] = Field(default=None, min_length=8)