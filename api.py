import requests,os,json,datetime

api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET']
api_endpoint = os.environ['API_ENDPOINT']
api_data_endpoint = os.environ['API_DATA_ENDPOINT']

headers = {
    'APCA-API-KEY-ID': api_key,
    'APCA-API-SECRET-KEY': api_secret,
    'accept': 'application/json',
    'content-type': 'application/json'
}


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

    response = requests.get(url, headers=headers)
    return response.text

def getAllOpenOrders():
    """
        retrieves all open orders
        eg: orders that are active, waiting for execution
    """
    url = f"{api_endpoint}/orders"
    
    response = requests.get(url, headers=headers)
    return response.text

def getLatestPrice(symbol=""):
    """
        get the latest price point of a certain symbol
    """

    url = f"{api_data_endpoint}/stocks/bars/latest?symbols={symbol}"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data["bars"][symbol]["c"]

def getPriceHistory(symbol, minutes):
    """
        Get the last 14 price points with a 15 minutes interval
    """
    # get date, calculate the starting point, and formatting it so the api can accept it
    now = datetime.datetime.now(datetime.timezone.utc)
    prev = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    nowstr = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    prevstr = prev.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


    # set the correct query parameters
    url = f"{api_data_endpoint}/stocks/bars"
    payload = {
        'symbols':symbol,
        'timeframe':f"{minutes}T",
        'start':prevstr,
        'end':nowstr,
        'limit':1000,
        'adjustment':'raw',
        'feed':'iex',
        'sort':'asc'
    }

    # make the request and filter out the stuff we dont need
    response = requests.get(url,payload, headers=headers)
    data = json.loads(response.text)
    result = []
    for price in data["bars"][symbol][-14:]:
        result.append(price["c"])
    return result

def isMarketOpen():
    url = f"{api_endpoint}/clock"
    
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data["is_open"]




# ====== dev functions ======
def getHeaders():
    print(headers)


# def createOrder(symbol="", qty=1, action="buy", type="market", tif="ioc"):
# def getAllOpenPositions():
# def getAllOpenOrders():
# def getLatestPrice(symbol=""):
# def getPriceHistory(symbol, minutes):
# def getHeaders():
