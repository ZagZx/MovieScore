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
    
@usuario_router.post("", response_model=UsuarioRead)
def criar_usuario(usuario_json: UsuarioCreate, session: SessionDep):
    novo_usuario = Usuario(
        nome=usuario_json.nome,
        email=usuario_json.email,
        senha_hash=get_password_hash(usuario_json.senha)
    )
    try:
        session.add(novo_usuario)
        session.commit()
    except:
        session.rollback()

    return novo_usuario

@usuario_router.patch("/{id}", response_model=UsuarioRead)
def atualizar_usuario(id: int, usuario_json: UsuarioUpdate, session: SessionDep):
    usuario = session.get(Usuario, id)
    
    if not usuario:
        raise HTTPException(status_code=404)
    
    if usuario_json.nome:
        usuario.nome = usuario_json.nome
    if usuario_json.email:
        usuario.email = usuario_json.email
    if usuario_json.senha:
        usuario.senha_hash = get_password_hash(usuario_json.senha)

    try: 
        session.commit()
        session.refresh(usuario)
    except:
        session.rollback()

    return usuario
    
@usuario_router.delete("/{id}")
def deletar_usuario(id: int, session: SessionDep):
    usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(status_code=404)
   
    session.delete(usuario)

    try:
        session.commit()
    except:
        session.rollback()

