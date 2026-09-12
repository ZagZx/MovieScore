from pydantic import EmailStr, Field, field_serializer
from typing import Optional
from datetime import datetime
from urllib.parse import urljoin

from constants import BASE_URL
from .base import Base


class UsuarioCreate(Base):
    nome: str = Field(min_length=3, max_length=50)
    email: EmailStr
    senha: str = Field(min_length=8)


class UsuarioRead(Base):
    id: int
    nome: str
    email: EmailStr
    foto_perfil_url: Optional[str] = Field(
        default=None, validation_alias="foto_perfil_path"
    )
    data_criacao: datetime

    @field_serializer("foto_perfil_url", when_used="json-unless-none")
    def adicionar_url_base_em_foto_perfil_url(self, foto_perfil_url: str):
        return urljoin(BASE_URL, foto_perfil_url).replace("\\", "/")


class UsuarioUpdate(Base):
    nome: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    senha: Optional[str] = Field(default=None, min_length=8)
