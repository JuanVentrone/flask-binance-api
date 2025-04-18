import requests
import time
import hmac
import hashlib
import configparser
import json

config = configparser.ConfigParser()
config.read('config.conf')

api_key = config['binance']['api_key']
secret_key = config['binance']['secret_key']

algo = "sha256"
# Algo es el tipo de hash que necesitamos revisar eso lo haremos cuando necesitemos hacer esto en diferentes pasos

def get_data(user_name, page_size=100, fixed_page=None):
    all_workers = []

    if fixed_page:
        # Solo una página específica
        timestamp = int(time.time() * 1000)
        params = f"algo=sha256&userName={user_name}&pageIndex={fixed_page}&pageSize={page_size}&timestamp={timestamp}&recvWindow=60000"
        signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()

        url = f"https://api.binance.com/sapi/v1/mining/worker/list?{params}&signature={signature}"
        headers = { "X-MBX-APIKEY": api_key }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data  # responde directo

    # Modo por defecto: traer todo paginado
    page = 1
    total_pages = 1

    while page <= total_pages:
        timestamp = int(time.time() * 1000)
        params = f"algo=sha256&userName={user_name}&pageIndex={page}&pageSize={page_size}&timestamp={timestamp}&recvWindow=60000"
        signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()

        url = f"https://api.binance.com/sapi/v1/mining/worker/list?{params}&signature={signature}"
        headers = { "X-MBX-APIKEY": api_key }

        response = requests.get(url, headers=headers)
        data = response.json()

        if "data" not in data or "workerDatas" not in data["data"]:
            break

        all_workers.extend(data["data"]["workerDatas"])

        if page == 1:
            total_num = data["data"].get("totalNum", 0)
            total_pages = math.ceil(total_num / page_size)

        page += 1

    return {
        "code": 0,
        "data": {
            "workerDatas": all_workers
        },
        "msg": ""
    }
