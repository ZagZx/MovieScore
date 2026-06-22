from fastapi import APIRouter, HTTPException, status

from constants import KITSU_API_URL, HEADERS_KITSU
from utils import get_data, ExternalAPIError

animes_router = APIRouter(prefix="/anime", tags=["anime"])


@animes_router.get("")
def buscar_animes(busca: str):
    url = KITSU_API_URL + "/anime"
    params = {}

    if busca:
        params["filter[text]"] = busca

    try:
        return get_data(url, params, HEADERS_KITSU)
    except ExternalAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)