from pathlib import Path
import os

import requests
from PIL import Image


def print_image(image_path, access_token):
    image_path = Path(image_path)
    pdf_path = f'{image_path.stem}.pdf'
    image = Image.open(image_path)
    image.save(pdf_path, "PDF", resolution=100.0, save_all=True)

    payload = {
        'jobName': 'demo', 'printMode': 'document',
        'printSettings': {
            'paperSize': 'ps_a4',
            'paperType': 'pt_plainpaper',
            'borderless': False,
            'printQuality': 'normal',
            'paperSource': 'auto',
            'colorMode': 'color',
            'doubleSided': 'none',
            'reverseOrder': True,
            'copies': 1,
            'collate': False
        }
    }
    headers = {
        'Authorization': f"Bearer {access_token}",
        'x-api-key': os.getenv('API_KEY'),
        'content-type': "application/json"
    }
    url = 'https://api.epsonconnect.com/api/2/printing/jobs'
    resp = requests.post(url, headers=headers, json=payload)
    job_id, upload_uri = resp.json()['jobId'], resp.json()['uploadUri']

    headers = {'Content-Type': 'application/octet-stream'}
    with open(pdf_path, 'rb') as file:
        file_data = file.read()
    requests.post(f"{upload_uri}&File={pdf_path}", headers=headers, data=file_data)

    headers = {
        'Authorization': f"Bearer {access_token}",
        'x-api-key': os.getenv('API_KEY'),
    }
    requests.post(f'https://api.epsonconnect.com/api/2/printing/jobs/{job_id}/print', headers=headers)

    os.remove(pdf_path)