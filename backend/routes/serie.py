from fastapi import APIRouter, HTTPException, status
from requests.exceptions import RequestException

from constants import (
    TMDB_API_URL,
    PARAMS_TMDB,
    HEADERS_TMDB
)
from utils import get_data


series_router = APIRouter(
    prefix="/series",
    tags=["Séries"]
)

@series_router.get("")
def buscar_series(busca: str):
    params = PARAMS_TMDB.copy()
    if busca:
        params["query"] = busca
        
    try:
        data = get_data(
            f"{TMDB_API_URL}/search/tv",
            params=params,
            headers=HEADERS_TMDB
        )


        if not data:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de séries indisponível no momento."
            )

        return data.get("results", [])

    except RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível conectar à API TMDB."
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao buscar séries."
        )


@series_router.get("/{serie_id}")
def buscar_serie(serie_id: int):
    try:
        data = get_data(
            f"{TMDB_API_URL}/tv/{serie_id}",
            params=PARAMS_TMDB,
            headers=HEADERS_TMDB
        )

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Série não encontrada."
            )

        if data.get("success") is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Série não encontrada."
            )

        return data

    except RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível conectar à API TMDB."
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao buscar série."
        )