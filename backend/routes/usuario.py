from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from database import SessionDep
from utils import get_password_hash
from models import Usuario
from services import UsuarioServiceDep
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate
)
from exceptions import NotFoundException

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("", response_model=list[UsuarioRead])
def listar_usuarios(usuario_service: UsuarioServiceDep):
    return usuario_service.list_usuario()

@usuario_router.get("/{id}", response_model=UsuarioRead)
def buscar_usuario(id: int, usuario_service: UsuarioServiceDep):
    return usuario_service.get_usuario(id)
    
@usuario_router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_json: UsuarioCreate, usuario_service: UsuarioServiceDep):
    usuario_existente = usuario_service.get_usuario_by_email(usuario_json.email)
    if usuario_existente:
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse email")

    usuario = usuario_service.create_usuario(usuario_json)

    return usuario

@usuario_router.patch("/{id}", response_model=UsuarioRead)
def atualizar_usuario(id: int, usuario_json: UsuarioUpdate, usuario_service: UsuarioServiceDep):
    return usuario_service.update_usuario(id, usuario_json)
    
@usuario_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(id: int, usuario_service: UsuarioServiceDep):
    usuario_service.delete_usuario(id)