import requests
import json

def get(url, params):
    response = requests.get(url)
    if response.ok:
        return json.loads(response.text)
    else:
        print("Ошибка при загрузке данных:", response.status_code)
        return None


def post(url, params):
    response = requests.post(url, params=params)
    if response.ok:
        return json.loads(response.text)
    else:
        print("Ошибка при загрузке данных:", response.status_code)
        return None