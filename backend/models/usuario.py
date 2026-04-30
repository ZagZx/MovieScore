from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UsuarioBase(SQLModel):
    nome: str = Field(unique=True)
    email: EmailStr = Field(unique=True)


class UsuarioUpdate(SQLModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioRead(UsuarioBase):
    id: int

class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    senha_hash: str