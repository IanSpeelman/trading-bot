import api, datetime

class Symbol:
    def __init__(self, symbol):
        self.average_gain = 0
        self.average_loss = 0
        self.last_update = 0
        self.amount = 0
        self.rsi = 0
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def updateRSI(self, data):
        """
            updates the RSI value for this symbol
            data is a list with the last prices sorted ASC
        """
        # if average_gain and average_loss are 0, we have not yet calculated any rsi,
        # so we need to do a clean calculation
        if self.average_loss == 0 and self.average_gain == 0:
            lastNumber = None
            gainTotal = 0
            lossTotal = 0
            for price in data:
                if lastNumber == None:
                    lastNumber = price
                    continue
                # calculate the difference between every adjecent price
                if lastNumber - price < 0:
                    gainTotal += abs(lastNumber - price)
                    lastNumber = price
                else:
                    lossTotal += abs(lastNumber - price)
                    lastNumber = price
            # calculate the average_gain and average_loss
            self.average_gain = gainTotal / len(data)
            self.average_loss = lossTotal / len(data)
        else:
            # if we got here, we already have an average_gain and average_loss
            # we need to re-calculate with smoothing
            lastPrices = data[-2:]
            if lastPrices[0] - lastPrices[1] < 0:
                self.average_gain = (self.average_gain * 13 + abs(lastPrices[0] - lastPrices[1])) / 14
            else:
                self.average_loss = (self.average_loss * 13 + abs(lastPrices[0] - lastPrices[1])) / 14


        # calculate relativeStrength and rsi, and round to 2 decimals
        relativeStrength = self.average_gain / self.average_loss
        self.rsi = round(100 - (100 / (1 + relativeStrength)), 2)

        return self.rsi

    def getRSI(self):
        return self.rsi

    def updateAmount(self):
        self.amount = api.getQTY(self.symbol)


class SymbolStore:
    def __init__(self):
        self.symbols = []

    def addSymbol(self, symbol):
        """
            Add a new symbol object with the given symbol name.
            returns the newly created symbol
            if the symbol already exists, it will return the already existing symbol without adding a new one
            symbol: [string]
        """
        symbol = symbol.upper()
        for storedSymbol in self.symbols:
            if symbol == storedSymbol.symbol:
                print('symbol already exists, this one is not added')
                return storedSymbol
        newSymbol = Symbol(symbol)
        self.symbols.append(newSymbol)
        return newSymbol
    
    def removeSymbol(self, symbol):
        """
            Remove symbol object from list
            returns the removed symbol
            symbol: [string]
        """
        symbol = symbol.upper()
        for storedSymbol in self.symbols:
            if storedSymbol.symbol == symbol:
                self.symbols.remove(storedSymbol)
                return symbol
        return False
    
    def getSymbol(self, symbol):
        """
            returns a Symbol object if it exists, otherwise it will return false
            symbol: [string]
        """
        symbol = symbol.upper()
        for storedSymbol in self.symbols:
            if storedSymbol.symbol == symbol:
                return storedSymbol
        return False

    def listAllSymbols(self):
        """
            return a list of all stored symbol objects
        """
        return self.symbols
    
    def updateAllSymbolRSI(self):
        """
            update the RSI values for all symbols
        """
        from index import interval
        symbols = []
        for symbol in self.symbols:
            symbols.append(symbol.symbol)

        data = api.getPriceHistory(symbols, interval[0])
        for symbol in self.symbols:
            symbol.updateRSI(data[symbol.symbol])

def checkForOpportunities(symbols):
    """
        check if there are any symbol for wich it makes sense to execute an order

    """
    # TODO: check for good rsi thresholds to start order
    # TODO: check for good rsi thresholds to end order
    from index import interval

    now = datetime.datetime.now(datetime.timezone.utc)
    closingTimeIntervalOffset = datetime.datetime.strptime(api.closingTime(), "%Y-%m-%dT%H:%M:%S%z") - datetime.timedelta(minutes=interval[0] + 1 )
    closing = now > closingTimeIntervalOffset

    if closing:
        print(f'[{str(now.time())[0:5]}] market is about to close, panic close now')
        api.panic()

    allSymbols = symbols.listAllSymbols()
    if api.isMarketOpen():
        print(f"\n\nSymbol\t RSI \t Action", end='')
        print(f'\n================ {str(now.time())[0:5]} ================', end='')
        for symbol in allSymbols:
            symbol.updateRSI(interval[0]);
            if symbol.getRSI() > 70:
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t Selling", end='')
                placeOrder(symbol, "sell")
            elif symbol.getRSI() < 30:
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t Buying", end='')
                placeOrder(symbol, "buy")
            else:
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t No action", end='')
        return True
    else:
        print("market is closed")
        return False

def placeOrder(symbol, action):
    """
        places an order based on symbol and action (sell or buy)
        determines if an order is nessasary based on how much we already own
    """
    # TODO: calculate  and execute stop order
    # TODO: calculate how much we should buy or sell based on avalable funds
    symbol.updateAmount()
    if (int(symbol.amount) >= 1 and action == "buy") or (int(symbol.amount) <= -1 and action == "sell"):
        return
    if int(symbol.amount) == 0:
        api.createOrder(symbol.symbol, 1, action)
    else:
        api.createOrder(symbol.symbol, 2, action)
