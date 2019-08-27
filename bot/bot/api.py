import json
import requests

api_url_base = 'http://127.0.0.1:8000/api/'

headers = {
    'Content-Type': 'application/json',
}


def fetch_api(endpoint):
    api_url = '{}{}'.format(api_url_base, endpoint)
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        return None

    data = json.loads(response.content.decode('utf-8'))
    return data
