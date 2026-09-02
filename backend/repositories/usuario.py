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

    def list_usuarios(self, last_id: int, limit: int) -> tuple[list[Usuario], bool]:
        "Retorna a lista de usuários e um booleano indicando se existem mais usuários"
        usuarios = self.session.scalars(
            select(Usuario)
            .where(Usuario.id > last_id)
            .order_by(Usuario.id)
            .limit(limit + 1)
        ).all()
        has_more = len(usuarios) > limit

        return (usuarios[:limit] if has_more else usuarios), has_more


UsuarioRepositoryDep = Annotated[UsuarioRepository, Depends(UsuarioRepository)]