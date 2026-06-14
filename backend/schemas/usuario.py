from pydantic import (
    EmailStr, 
    Field, 
    BaseModel, 
    model_validator
)
from typing import Optional
from datetime import datetime
from os import path

from constants import API_URL


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

    @model_validator(mode="after")
    def corrigir_foto_url(self) -> "UsuarioRead":
        if self.foto_perfil_url:
            self.foto_perfil_url = path.join(API_URL, self.foto_perfil_url)
        
        return self

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    senha: Optional[str] = Field(default=None, min_length=8)