import requests
from datetime import datetime, timezone
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def get_now_datetime_utc():
    '''
    Retorna no formato UTC (Tempo Universal Coordenado), o datetime do momento em que a função for executada.
    
    OBS: Necessário converter para o horário do usuário no FrontEnd.
    '''
    return datetime.now(timezone.utc)

def get_data(url, params=None, headers=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:
        return None