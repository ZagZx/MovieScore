from sqlalchemy import select
from pwdlib import PasswordHash

from database import SessionDep
from models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from services.usuario_service import UsuarioService
from exceptions import (
    NotFoundException,
    ConflictException
)

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


class UsuarioServiceImpl(UsuarioService):
    def __init__(self, session: SessionDep):
        self.session = session

    def create_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nome = usuario_data.nome,
            email = usuario_data.email,
            senha_hash = get_password_hash(usuario_data.senha),
            foto_perfil_url = None # FALTA IMPLEMENTAR
        )

        try:    
            self.session.add(usuario)
            self.session.commit()
            self.session.refresh(usuario)
    
            return usuario
        except Exception:
            self.session.rollback()
            
            raise

    def delete_usuario(self, id: int):
        usuario = self.get_usuario(id)

        try:
            self.session.delete(usuario)
            self.session.commit()
        except Exception:
            self.session.rollback()

            raise 

    def update_usuario(self, id: int, usuario_data: UsuarioUpdate) -> Usuario:
        usuario = self.get_usuario(id)

        if self.get_usuario_by_email(usuario_data.email):
            raise ConflictException("Já existe um usuário com esse email")

        if usuario_data.nome:
            usuario.nome = usuario_data.nome
        if usuario_data.email:
            usuario.email = usuario_data.email
        if usuario_data.senha:
            usuario.senha_hash = get_password_hash(usuario_data.senha)
        if usuario_data.foto_perfil: # FALTA IMPLEMENTAR
            pass

        try: 
            self.session.commit()
            self.session.refresh(usuario)
            
            return usuario
        except Exception:
            self.session.rollback()
            
            raise

    def list_usuario(self) -> list[Usuario]:
        usuarios = self.session.scalars(
            select(Usuario)
        ).all()

        return usuarios
    
    def get_usuario(self, id: int) -> Usuario:
        usuario = self.session.get(Usuario, id)
        if not usuario:
            raise NotFoundException("Usuário", id)
        
        return usuario
        
    def get_usuario_by_email(self, email) -> Usuario | None:
        usuario = self.session.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        return usuario