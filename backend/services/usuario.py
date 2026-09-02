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

    try:
        conteudo = imagem.file.read()
    except OSError as exc:
        raise RuntimeError("Não foi possível ler a imagem enviada") from exc

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
        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(conteudo)
    except OSError as exc:
        deletar_imagem(str(caminho_arquivo))
        raise RuntimeError("Não foi possível salvar a imagem") from exc

    return str(caminho_arquivo)


def deletar_imagem(path: str):
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
        except OSError:
            print("Erro ao deletar imagem no caminho:", path)


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

        if usuario_data.email and usuario_data.email != usuario.email:
            if self.get_usuario_by_email(usuario_data.email):
                raise ConflictException("Já existe um usuário cadastrado com esse email")
            usuario.email = usuario_data.email
        if usuario_data.nome:
            usuario.nome = usuario_data.nome
        if usuario_data.senha:
            usuario.senha_hash = get_password_hash(usuario_data.senha)

        return self.usuario_repository.update_usuario(usuario)

    def update_foto_perfil(self, id: int, foto_perfil: UploadFile) -> Usuario:
        usuario = self.get_usuario(id)

        caminho_foto_antiga = usuario.foto_perfil_path
        caminho_foto_nova = salvar_imagem(foto_perfil)

        usuario.foto_perfil_path = caminho_foto_nova

        try:
            usuario = self.usuario_repository.update_foto_perfil(usuario)
        except Exception:
            deletar_imagem(caminho_foto_nova)
            raise
        deletar_imagem(caminho_foto_antiga)

        return usuario

    def list_usuarios(self, last_id: int, limit: int) -> tuple[Sequence[Usuario], CursorPaging]:
        usuarios, has_more = self.usuario_repository.list_usuarios(last_id, limit)

        cursor = usuarios[-1].id if usuarios else None

        paging = CursorPaging(cursor=cursor, has_more=has_more)

        return usuarios, paging


UsuarioServiceDep = Annotated[UsuarioService, Depends(UsuarioService)]
