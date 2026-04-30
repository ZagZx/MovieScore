from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database import SessionDep
from models import UsuarioRead, UsuarioCreate, UsuarioUpdate, Usuario
from utils import get_password_hash

usuario_router = APIRouter(prefix="/usuario", tags=["usuario"])

@usuario_router.get("", response_model=list[UsuarioRead])
def listar_usuarios(session: SessionDep):
    usuarios = session.exec(
        select(Usuario)
    ).all()

    return usuarios

@usuario_router.get("/{id}", response_model=UsuarioRead)
def buscar_usuario(id: int, session: SessionDep):
    usuario: Usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(status_code=404)
    
    return usuario
    
@usuario_router.post("")
def criar_usuario(usuario: UsuarioCreate, session: SessionDep):
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=get_password_hash(usuario.senha)
    )
    try:
        session.add(novo_usuario)
        session.commit()
    except:
        session.rollback()
