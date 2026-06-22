import requests
from datetime import datetime, timezone
from pwdlib import PasswordHash
from requests.exceptions import (
    ConnectionError,
    Timeout,
    TooManyRedirects,
    HTTPError,
    RequestException,
)

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


def get_now_datetime_utc():
    """
    Retorna no formato UTC (Tempo Universal Coordenado), o datetime do momento
    em que a função for executada.

    OBS: Necessário converter para o horário do usuário no FrontEnd.
    """
    return datetime.now(timezone.utc)


class ExternalAPIError(Exception):
    """
    Exceção genérica para erros de APIs externas.

    Atributos:
        message  – mensagem legível para logs / respostas HTTP
        status_code – código HTTP sugerido para repassar ao cliente
    """

    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def get_data(url: str, params: dict | None = None, headers: dict | None = None) -> dict:
    """
    Realiza uma requisição GET para uma API externa e retorna o JSON.

    Lança ExternalAPIError em vez de retornar None, permitindo que as rotas
    propaguem o erro com contexto adequado.

    Raises:
        ExternalAPIError: em qualquer falha de rede, timeout ou resposta HTTP
                          com status de erro (4xx / 5xx).
    """
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except Timeout:
        raise ExternalAPIError(
            f"A API externa demorou demais para responder: {url}",
            status_code=504,
        )
    except ConnectionError:
        raise ExternalAPIError(
            f"Não foi possível conectar à API externa: {url}",
            status_code=502,
        )
    except TooManyRedirects:
        raise ExternalAPIError(
            f"Muitos redirecionamentos ao acessar a API externa: {url}",
            status_code=502,
        )
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 0
        if status == 401:
            raise ExternalAPIError(
                "Chave de API inválida ou sem permissão de acesso.",
                status_code=502,
            )
        if status == 404:
            raise ExternalAPIError(
                "Recurso não encontrado na API externa.",
                status_code=404,
            )
        if status == 429:
            raise ExternalAPIError(
                "Limite de requisições da API externa atingido. Tente novamente mais tarde.",
                status_code=429,
            )
        if status >= 500:
            raise ExternalAPIError(
                f"A API externa retornou um erro interno (HTTP {status}).",
                status_code=502,
            )
        raise ExternalAPIError(
            f"Erro HTTP {status} ao acessar a API externa.",
            status_code=502,
        )
    except RequestException as exc:
        raise ExternalAPIError(
            f"Erro inesperado ao acessar a API externa: {exc}",
            status_code=502,
        )