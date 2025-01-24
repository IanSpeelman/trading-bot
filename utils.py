import api

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

    def updateRSI(self, interval=15):
        # TODO:
        # keep track of when RSI is last updated in last_update variable
        data = api.getPriceHistory(self.symbol, interval) # this now gets the latest 14 price points with interval minutes interval
        if(self.average_loss == 0 and self.average_gain == 0):
            lastNumber = None
            gainTotal = 0
            lossTotal = 0
            for price in data:
                if(lastNumber == None):
                    lastNumber = price
                    continue
            
                if(lastNumber - price < 0):
                    gainTotal += abs(lastNumber - price)
                    lastNumber = price
                else:
                    lossTotal += abs(lastNumber - price)
                    lastNumber = price
            self.average_gain = gainTotal / 14
            self.average_loss = lossTotal / 14
        else:
            lastPrices = data[-2:]
            if(lastPrices[0] - lastPrices[1] < 0):
                self.average_gain = (self.average_gain * 13 + abs(lastPrices[0] - lastPrices[1])) / 14
            else:
                self.average_loss = (self.average_loss * 13 + abs(lastPrices[0] - lastPrices[1])) / 14


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
            if(symbol == storedSymbol.symbol ):
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
            if(storedSymbol.symbol == symbol):
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
            if(storedSymbol.symbol == symbol):
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
        for symbol in self.symbols:
            symbol.updateRSI()
            print(f"updated RSI value for: {symbol}")


def checkForBets(symbols):
    """
        check if there are any symbol for wich it makes sense to execute an order
    """
    # TODO: check for good rsi thresholds to start order
    # TODO: check for good rsi thresholds to end order
    from index import interval
    allSymbols = symbols.listAllSymbols()
    if(api.isMarketOpen()):
        print(f"\n\nSymbol\t RSI \t Action", end='')
        print('\n=======================================================================', end='')
        for symbol in allSymbols:
            symbol.updateRSI(interval[0]);
            if(symbol.getRSI() > 70):
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t Selling", end='')
                placeOrder(symbol, "sell")
            elif(symbol.getRSI() < 30):
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t Buying", end='')
                placeOrder(symbol, "buy")
            else:
                print(f"\n{symbol.symbol}\t {symbol.getRSI()}\t No action", end='')
    else:
        print("market is closed")

def placeOrder(symbol, action):
    # TODO: calculate  and execute stop order
    symbol.updateAmount()
    if((int(symbol.amount) >= 1 and action == "buy") or (int(symbol.amount) <= -1 and action == "sell")):
        return
    if(int(symbol.amount) == 0):
        api.createOrder(symbol.symbol, 1, action)
    else:
        api.createOrder(symbol.symbol, 2, action)


# def __init__(self, symbol): ==== Symbol class ====
# def updateRSI(self):
# def getRSI(self):
#
# def __init__(self):       ==== SymbolStore class ====
# def addSymbol(self, symbol): def removeSymbol(self, symbol):
# def getSymbol(self, symbol):
# def listAllSymbols(self):
# def updateAllSymbolRSI(self):
