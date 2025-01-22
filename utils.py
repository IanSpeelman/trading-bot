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

    
    """
        TODO: 
        calculate rsi function 
        get historical prices
        get current date and have the ability to caculate with it
        in the request to get historical prices, the end will be current time, and start will be step time * 14 before end time
        make sure to smooth the average gain/loss if these numbers are known, if these numbers are unknown calculate the raw one, and smooth as we go

        calculate the RSI value for a specific symbol
        symbol: [string] the symbol to calculate the RSI value for
        periodLength: [number] time in minutes as the interval for periods
    """

    def updateRSI(self):
        # TODO:
        # update average_gain / average_loss / last_update
        data = api.getPriceHistory(self.symbol, 15) # this now gets the latest 14 price points with 15 minutes interval
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
        self.rsi = 100 - (100 / (1 + relativeStrength))

        return self.rsi


    def getRSI(self):
        return self.rsi


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
        for storedSymbol in self.symbols:
            if(symbol is storedSymbol.symbol ):
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
        for storedSymbol in self.symbols:
            if(storedSymbol.symbol is symbol):
                self.symbols.remove(storedSymbol)
                return symbol
        return False
    
    def getSymbol(self, symbol):
        """
            returns a Symbol object if it exists, otherwise it will return false
            symbol: [string]
        """
        for storedSymbol in self.symbols:
            if(storedSymbol.symbol is symbol):
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


    # def __init__(self, symbol): ==== Symbol class ====
    # def __str__(self):
    # def updateRSI(self):
    # def getRSI(self):
    #
    # def __init__(self):       ==== SymbolStore class ====
    # def addSymbol(self, symbol):
    # def removeSymbol(self, symbol):
    # def getSymbol(self, symbol):
    # def listAllSymbols(self):
    # def updateAllSymbolRSI(self):
