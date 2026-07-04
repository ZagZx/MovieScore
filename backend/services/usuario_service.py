from fastapi import UploadFile
from abc import ABC, abstractmethod

from models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate


class UsuarioService(ABC):
    @abstractmethod
    def create_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        pass

    @abstractmethod
    def delete_usuario(self, id: int):
        pass

    @abstractmethod
    def update_usuario(self, id: int, usuario_data: UsuarioUpdate) -> Usuario:
        pass

    @abstractmethod
    def update_foto_perfil(self, id, foto_perfil: UploadFile) -> Usuario:
        pass

    from schemas.pagination import CursorPaging
    @abstractmethod
    def list_usuario(self, last_id: int, limit: int) -> tuple[list[Usuario], CursorPaging]:
        pass

    @abstractmethod
    def get_usuario(self, id: int) -> Usuario:
        pass

    @abstractmethod
    def get_usuario_by_email(self, email: str) -> Usuario | None:
        pass
