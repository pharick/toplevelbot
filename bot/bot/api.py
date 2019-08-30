import json
import requests


class Api:
    url_base = 'http://127.0.0.1:8000/api/'

    headers = {
        'Content-Type': 'application/json',
    }

    @staticmethod
    def get(endpoint, args={}):
        arg_strings = '&'.join(['='.join([str(arg[0]), str(arg[1])]) for arg in args.items()])
        api_url = '{}{}/?{}'.format(Api.url_base, endpoint, arg_strings)
        response = requests.get(api_url, headers=Api.headers)
        data = json.loads(response.content.decode('utf-8'))
        return data

    @staticmethod
    def post(endpoint, data):
        api_url = '{}{}/'.format(Api.url_base, endpoint)
        response = requests.post(api_url, headers=Api.headers, json=data)
        data = json.loads(response.content.decode('utf-8'))
        return data
