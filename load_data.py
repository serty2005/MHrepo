import requests
import json

def load_data(url):
    response = requests.get(url)
    if response.ok:
        return json.loads(response.text)
    else:
        print("Ошибка при загрузке данных:", response.status_code)
        return None