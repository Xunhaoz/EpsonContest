import os
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
    }

    data = {
        'grant_type': 'authorization_code',
        'code': request.query_params.get('code'),
        'redirect_uri': os.getenv('DOMAIN') + '/callback',
    }

    resp = requests.post(os.getenv('TOKEN_URL'), headers=headers, data=data)
    resp.raise_for_status()
    tokens = resp.json()
    return tokens


def get_user_printer(access_token: str):
    header = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': os.getenv('API_KEY')
    }
    response = requests.get('https://api.epsonconnect.com/api/2/printing/devices/info', headers=header)

    return response.json()['productName'], response.json()['serialNumber'], response.json()['connected']


def check_user_scanner(access_token: str):
    headers = {
        'Authorization': f"Bearer {access_token}",
        'x-api-key': os.getenv('API_KEY'),
    }
    url = 'https://api.epsonconnect.com/api/2/scanning/destinations'
    response = requests.get(url, headers=headers).json()

    for payload in response['destinations']:
        requests.delete(f"{url}/{payload['destinationId']}", headers=headers)

    payload = {
        "aliasName": "demoWebsite", "destinationService": "url",
        "destination": f"{os.getenv('DOMAIN')}/scanning_destinations"}
    requests.post(url, headers=headers, json=payload).json()
    return
