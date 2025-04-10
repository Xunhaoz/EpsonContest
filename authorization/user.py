import os
import time
import base64

from fastapi import Request
import requests


def get_user(request: Request):
    user = request.session.get('user')
    return user['name'] if user else None


def get_user_tokens(request: Request):
    credentials = f"{os.getenv('CLIENT_ID')}:{os.getenv('CLIENT_SECRET')}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': request.query_params.get('code'),
        'redirect_uri': os.getenv('REDIRECT_URI')
    }

    resp = requests.post(os.getenv('TOKEN_URL'), headers=headers, data=data)
    resp.raise_for_status()
    tokens = resp.json()
    tokens['expires_at'] = tokens['expires_in'] + int(time.time()) - 60
    return tokens
