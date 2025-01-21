import requests,os

api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET']
api_endpoint = os.environ['API_ENDPOINT']
api_data_endpoint = os.environ['API_DATA_ENDPOINT']

def createOrder(symbol="", qty=1, action="buy", type="market", tif="ioc"):
    """
        =============================================================
        creates a new order with the given requirements
        =============================================================
        symbol: represents what stock we want to interact with
        qty: represents the amount of that symbol we want to interact with
        action: if we want to 'buy' or 'sell' this position
        type: is an enum, options are 'market' limit' 'stop_limit' 'trailing_stop'
        tif: time in force, is another enum, options are 'day' 'gtc' 'opg' 'cls' 'ioc' 'fok'

        this function is reponsible for placing a new order
    """

    url = f"{api_endpoint}/orders"

    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret,
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    data = {
        "side": action,
        "type": type,
        "time_in_force": tif,
        "symbol": symbol,
        "qty": str(qty)
    }

    response = requests.post(url, json=data, headers=headers)
    return response.text



def getAllOpenPositions():
    """
        retrieves all open positions
    """    
    url = f"{api_endpoint}/positions"
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret,
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return response.text

def getAllOpenOrders():
    """
        retrieves all open orders
        eg: orders that are active, waiting for execution
    """
    url = f"{api_endpoint}/orders"
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret,
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return response.text

def getLatestPrice(symbol=""):
    """
        get the latest price point of a certain symbol
    """

    url = f"{api_data_endpoint}/stocks/quotes/latest?symbols={symbol}"

    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret,
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return response.text

# ====== dev functions ======
def getHeaders():
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    print(headers)
