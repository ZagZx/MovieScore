from typing import Annotated
from sqlalchemy import select
from fastapi import Depends

from database import SessionDep
from models import Usuario

class UsuarioRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_usuario(self, id: int) -> Usuario | None:
        usuario = self.session.get(Usuario, id)
        return usuario

    def get_usuario_by_email(self, email: str) -> Usuario | None:
        usuario = self.session.scalar(
            select(Usuario).where(Usuario.email == email)
        )
        return usuario
    
    def create_usuario(self, usuario: Usuario):
        try:
            self.session.add(usuario)
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except Exception:
            self.session.rollback()
            raise

    def delete_usuario(self, usuario: Usuario):
        try:
            self.session.delete(usuario)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def update_usuario(self, usuario: Usuario):
        try:
            self.session.commit()
            self.session.refresh(usuario)

            return usuario
        except Exception:
            self.session.rollback()
            raise

    def update_foto_perfil(self, usuario: Usuario) -> Usuario:
        try:
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except Exception:
            self.session.rollback()
            raise


UsuarioRepositoryDep = Annotated[UsuarioRepository, Depends(UsuarioRepository)]