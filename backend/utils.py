import requests
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def get_data(url, params = None, headers = None):
    request = requests.get(url, params, headers=headers)

    try:
        data = request.json()
    except Exception as e:
        print(e)

    return data