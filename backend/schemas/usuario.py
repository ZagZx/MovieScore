from pydantic import EmailStr, Field, field_serializer
from typing import Optional
from datetime import datetime

from mappers.usuario import UsuarioMapper
from .base import Base


class UsuarioCreate(Base):
    nome: str = Field(min_length=3, max_length=50)
    email: EmailStr
    senha: str = Field(min_length=8)


class UsuarioRead(Base):
    id: int
    nome: str
    email: EmailStr
    sobre_mim: Optional[str] = Field(default=None)
    foto_perfil_url: Optional[str] = Field(
        default=None, validation_alias="foto_perfil_path"
    )
    data_criacao: datetime

    @field_serializer("foto_perfil_url", when_used="json-unless-none")
    def adicionar_url_base_em_foto_perfil_url(self, foto_perfil_url: str):
        return UsuarioMapper.map_foto_perfil(foto_perfil_url)


class UsuarioUpdate(Base):
    nome: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    senha: Optional[str] = Field(default=None, min_length=8)
    sobre_mim: Optional[str] = Field(default=None, max_length=1000)
