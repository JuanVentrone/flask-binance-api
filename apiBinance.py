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

def get_data(user_name):
    timestamp = int(time.time() * 1000)
    recv_window = 5000
    params = f"algo={algo}&userName={user_name}&timestamp={timestamp}&recvWindow={recv_window}"
    signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()

    url = f"https://api.binance.com/sapi/v1/mining/worker/list?{params}&signature={signature}"

    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.get(url, headers=headers)
    
    # print(response.json())
    return response.json()