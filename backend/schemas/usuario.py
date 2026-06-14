from pydantic import (
    EmailStr, 
    Field, 
    BaseModel, 
    field_serializer
)
from typing import Optional
from datetime import datetime
from urllib.parse import urljoin

from constants import BASE_URL


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=50)
    email: EmailStr
    senha: str = Field(min_length=8)

class UsuarioRead(BaseModel):
    id: int
    nome: str
    email: EmailStr
    foto_perfil_url: Optional[str]
    data_criacao: datetime

    @field_serializer("foto_perfil_url", when_used="json-unless-none")
    def adicionar_url_base_em_foto_perfil_url(self, foto_perfil_url: Optional[str]):
        return urljoin(BASE_URL, foto_perfil_url)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    senha: Optional[str] = Field(default=None, min_length=8)