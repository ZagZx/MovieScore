from dotenv import load_dotenv
from os import getenv


STORAGE = "storage"
STORAGE_FOTOS_PERFIL = STORAGE + "/usuarios/fotos"

load_dotenv()


KITSU_API_URL = "https://kitsu.io/api/edge"
TMDB_API_URL = "https://api.themoviedb.org/3"

TMDB_KEY = getenv("TMDB_API_KEY")
if not TMDB_KEY:
    raise ValueError("TMDB_API_KEY não encontrada no arquivo .env")

BASE_URL = getenv("BASE_URL") # utilizada no retorno da foto_perfil_url do usuário
if not BASE_URL:
    raise ValueError("BASE_URL não encontrado no arquivo .env")

PARAMS_TMDB = {
    "language": "pt-BR"
}
HEADERS_TMDB = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_KEY}"
}

HEADERS_KITSU = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}