import magic
import os
from typing import Sequence, Annotated
from fastapi import UploadFile, Depends
from sqlalchemy import select
from pathlib import Path
from uuid import uuid4

from auth import get_password_hash
from constants import STORAGE
from models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from schemas.pagination import CursorPaging
from repositories import UsuarioRepositoryDep
from exceptions import (
    NotFoundException,
    ConflictException,
    UnsupportedMediaTypeException,
)


def salvar_imagem(imagem: UploadFile) -> str:
    "Salva a imagem no storage e retorna o caminho para ela"
    TIPOS_PERMITIDOS = ["image/png", "image/jpeg", "image/webp"]
    EXTENSOES_PERMITIDAS = [".jpg", ".jpeg", ".png", ".webp"]

    conteudo = imagem.file.read()
    mime_type = magic.from_buffer(conteudo[:2048], mime=True)
    if mime_type not in TIPOS_PERMITIDOS:
        raise UnsupportedMediaTypeException(
            f"Tipo {mime_type} não suportado, use JPEG, PNG ou WebP"
        )

    extensao = Path(imagem.filename).suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise UnsupportedMediaTypeException(
            f"Extensão {extensao} não suportada, use .jpg, .jpeg, .png ou .webp"
        )

    caminho = Path(STORAGE)
    nome_arquivo = uuid4().hex + extensao

    caminho_arquivo = caminho.joinpath(Path(nome_arquivo))

    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
    except Exception:
        raise

    return str(caminho_arquivo)


def deletar_imagem(path: str):
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Erro ao deletar imagem {path}: {e}")


class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepositoryDep):
        self.usuario_repository = usuario_repository

    def get_usuario(self, id: int) -> Usuario:
        usuario = self.usuario_repository.get_usuario(id)
        if not usuario:
            raise NotFoundException("Usuário", id)

        return usuario

    def get_usuario_by_email(self, email: str) -> Usuario | None:
        usuario = self.usuario_repository.get_usuario_by_email(email)

        return usuario

    def create_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        if self.usuario_repository.get_usuario_by_email(usuario_data.email):
            raise ConflictException("Já existe um usuário cadastrado com esse email")

        usuario = Usuario(
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha_hash=get_password_hash(usuario_data.senha),
        )

        return self.usuario_repository.create_usuario(usuario)

    def delete_usuario(self, id: int):
        usuario = self.usuario_repository.get_usuario(id)
        caminho_foto = usuario.foto_perfil_path

        self.usuario_repository.delete_usuario(usuario)

        try:
            deletar_imagem(caminho_foto)
        except Exception:
            raise

    def update_usuario(self, id: int, usuario_data: UsuarioUpdate) -> Usuario:
        usuario = self.get_usuario(id)

        if self.get_usuario_by_email(usuario_data.email):
            raise ConflictException("Já existe um usuário cadastrado com esse email")

        if usuario_data.nome:
            usuario.nome = usuario_data.nome
        if usuario_data.email:
            usuario.email = usuario_data.email
        if usuario_data.senha:
            usuario.senha_hash = get_password_hash(usuario_data.senha)

        try:
            self.session.commit()
            self.session.refresh(usuario)

            return usuario
        except Exception:
            self.session.rollback()

            raise

    def update_foto_perfil(self, id: int, foto_perfil: UploadFile) -> Usuario:
        usuario = self.get_usuario(id)

        caminho_foto_antiga = usuario.foto_perfil_path
        caminho_foto_nova = salvar_imagem(foto_perfil)

        usuario.foto_perfil_path = caminho_foto_nova

        try:
            self.session.commit()
            self.session.refresh(usuario)
        except Exception:
            self.session.rollback()
            deletar_imagem(caminho_foto_nova)

            raise
        deletar_imagem(caminho_foto_antiga)

        return usuario

    def list_usuario(
        self, last_id: int, limit: int
    ) -> tuple[Sequence[Usuario], CursorPaging]:
        last_id_table = self.session.scalar(
            select(Usuario.id).order_by(Usuario.id.desc()).limit(1)
        )

        usuarios = []
        if last_id < last_id_table:
            usuarios = self.session.scalars(
                select(Usuario).where(Usuario.id > last_id).limit(limit + 1)
            ).all()

        has_more = len(usuarios) > limit
        if has_more:
            usuarios[:limit]
        cursor = usuarios[len(usuarios) - 1].id if usuarios else None

        paging = CursorPaging(cursor=cursor, has_more=has_more)

        return usuarios, paging


    
UsuarioServiceDep = Annotated[UsuarioService, Depends(UsuarioService)]
