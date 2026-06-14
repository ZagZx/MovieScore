import magic
import os
from fastapi import UploadFile
from sqlalchemy import select
from pwdlib import PasswordHash
from pathlib import Path
from uuid import uuid4

from constants import STORAGE
from database import SessionDep
from models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from services.usuario_service import UsuarioService
from exceptions import (
    NotFoundException,
    ConflictException,
    UnsupportedMediaTypeException
)

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def salvar_imagem(imagem: UploadFile) -> str:
    "Salva a imagem no storage e retorna o caminho para ela"
    TIPOS_PERMITIDOS = ["image/png", "image/jpeg", "image/webp"]
    EXTENSOES_PERMITIDAS = [".jpg", ".jpeg", ".png", ".webp"]

    conteudo = imagem.file.read()
    mime_type = magic.from_buffer(conteudo[:2048], mime=True)
    if mime_type not in TIPOS_PERMITIDOS:
        raise UnsupportedMediaTypeException(f"Tipo {mime_type} não suportado, use JPEG, PNG ou WebP")
    
    extensao = Path(imagem.filename).suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise UnsupportedMediaTypeException(f"Extensão {extensao} não suportada, use .jpg, .jpeg, .png ou .webp")
    
    caminho = Path(STORAGE)
    nome_arquivo = uuid4().hex + extensao
    
    caminho_arquivo = caminho.joinpath(Path(nome_arquivo))

    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)    
    except Exception:
        raise 

    return str(caminho_arquivo)

class UsuarioServiceImpl(UsuarioService):
    def __init__(self, session: SessionDep):
        self.session = session

    def create_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        if self.get_usuario_by_email(usuario_data.email):
            raise ConflictException("Já existe um usuário cadastrado com esse email")

        usuario = Usuario(
            nome = usuario_data.nome,
            email = usuario_data.email,
            senha_hash = get_password_hash(usuario_data.senha)
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

    def update_foto_perfil(self, id:int, foto_perfil: UploadFile) -> Usuario:
        usuario = self.get_usuario(id)

        caminho_foto_antiga = usuario.foto_perfil_url
        caminho_foto_nova = salvar_imagem(foto_perfil)

        usuario.foto_perfil_url = caminho_foto_nova

        try:
            self.session.commit()
            self.session.refresh(usuario)
        except Exception:
            self.session.rollback()
            try:
                os.remove(caminho_foto_nova)
            except Exception as e:
                print(f"Erro ao deletar foto de perfil nova {caminho_foto_antiga}: {e}")

            raise

        if caminho_foto_antiga:
            if os.path.exists(caminho_foto_antiga):
                try:
                    os.remove(caminho_foto_antiga)
                except Exception as e:
                    print(f"Erro ao deletar foto de perfil antiga {caminho_foto_antiga}: {e}")
        return usuario     

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