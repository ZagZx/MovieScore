from urllib.parse import urljoin

from constants import BASE_URL


class UsuarioMapper:
    @staticmethod
    def map_foto_perfil(foto_perfil_path: str | None) -> str | None:
        if foto_perfil_path:
            return urljoin(BASE_URL, foto_perfil_path).replace("\\", "/")
