import requests,os,json,datetime,webbrowser

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

def createOrder(symbol="", qty=1, action="buy", type="trailing_stop", tif="day", trailing_percent=2):
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
    "type": "market",
    "time_in_force": tif,
    "symbol": symbol,
    "qty": str(qty),
    "side": action
    }

    response = requests.post(url, json=data, headers=headers)

    if(action == "buy"):
        action = "sell"
    else:
        action = "buy"


    data = {
    "type": type,
    "time_in_force": tif,
    "symbol": symbol,
    "qty": str(qty),
    "side": action,
    "trail_percent": str(trailing_percent)
    }

    response = requests.post(url, json=data, headers=headers)
    return response.text

def getQTY(symbol):
    """
        retrieves the amount of stocks we own for a symbol
    """
    url = f"{api_endpoint}/positions/{symbol}"

    info = requests.get(url, headers=headers)
    info = json.loads(info.text)
    try:
        return info["qty"]
    except:
        return 0


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

def getPriceHistory(listOfSymbols=[], minutes=15):
    """
        Get the last 14 price points with a interval minutes interval
    """
    # get date, calculate the starting point, and formatting it so the api can accept it
    now = datetime.datetime.now(datetime.timezone.utc)
    prev = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)
    nowstr = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    prevstr = prev.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
 
    symbols = ""
    for symbol in listOfSymbols:
        symbols = symbols + "," + symbol

    symbols = symbols[1:]

    url = f"{api_data_endpoint}/stocks/bars"
    payload = {
        'symbols':symbols,
        'timeframe':f"{minutes}T",
        'start':prevstr,
        'end':nowstr,
        'limit':1000,
        'feed':'iex',
        'sort':'asc'
    }

    # make the request and filter out the stuff we dont need
    response = requests.get(url,payload, headers=headers)
    data = json.loads(response.text)
    result = {}

    for symbol in listOfSymbols:
        try:
            for price in data["bars"][f"{symbol}"][-14:]:
                print(price)
                if not result.get(symbol):
                    result[f"{symbol}"] = []
                result[f"{symbol}"].append(price["c"])
        except NameError:
            print(f"{symbol} not found in data")
        except:
            print("something went wrong")


    return result

def isMarketOpen():
    """
        returns True if market is open, otherwise it returns False
    """
    # TODO: needs to check for each individual symbol, as we are failing for crypto
    url = f"{api_endpoint}/clock"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data["is_open"]

def panic():
    """
        Liquidates all open positions, and cancels all orders
    """
    orders = requests.delete(f"{api_endpoint}/orders", headers=headers)
    positions = requests.delete(f"{api_endpoint}/positions", headers=headers)
    orders = json.loads(orders.text)
    positions = json.loads(positions.text)
    url = "https://app.alpaca.markets"

    if len(orders) == 0 and len(positions) == 0 :
        return True

    for order in orders:
        print(order["status"])
        if order["status"] != 200 :
            webbrowser.open(url, new=0, autoraise=True)
            return False

    for position in positions:
        print(position["status"])
        if position["status"] != 200 :
            webbrowser.open(url, new=0, autoraise=True)
            return False

    return True

def closingTime():
    url = f"{api_endpoint}/clock"
    response = requests.get(url, headers=headers)
    time = json.loads(response.text)["next_close"]
    return time

def openTime():
    url = f"{api_endpoint}/clock"
    response = requests.get(url, headers=headers)
    time = json.loads(response.text)["next_open"]
    return time
