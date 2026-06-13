from typing import Annotated
from fastapi import Depends

from ..implementations.usuario_service_impl import UsuarioServiceImpl
from ..usuario_service import UsuarioService

UsuarioServiceDep = Annotated[UsuarioService, Depends(UsuarioServiceImpl)]