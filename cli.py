import os
import sys
import api
from index import trading, interval


def showOptions(msg="", clear=True):
    if clear:
        if sys.platform in ("linux", "dawin"):
            os.system("clear")
        else:
            os.system("cls")

    print(msg)
    print('1) Start Trading')
    print('2) Stop Trading')
    print('3) Change interval')
    print('4) Add symbol')
    print('5) Remove symbol')
    print('6) Panic (liquidate all open positions and cancel all remaining orders)')
    print('q) Quit')
    print("====================== settings ======================")
    print(f"Using account: {os.environ["ACCOUNT_NAME"]}")
    print(f"interval: {interval[0]}")
    print(f"trading: {trading.is_set()}")
    print(allSymbols())
    selection = input("Select option: ")

    match selection:
        case "1":
            startTrading()
        case "2":
            stopTrading()
        case "3":
            changeInterval()
        case "4":
            addSymbol()
        case "5":
            removeSymbol()
        case "6":
            panic()
        case "c":
            custom()
        case "q":
            exit(0)
        case _:
            showOptions("whoops, I didn't understand that one, you can try again")

def startTrading():
    trading.set()
    showOptions("trading started")

def stopTrading():
    global trading
    trading.clear()
    showOptions("trading stopped")

def changeInterval():
    interval[0] = int(input("new interval in minutes: "))
    showOptions(f"interval changed to {interval[0]} minutes")

def addSymbol():
    from index import symbols
    symbol = input("What symbol do you want to add: ")
    symbols.addSymbol(symbol.upper())
    showOptions(f"symbol '{symbol.upper()}' added")

def removeSymbol():
    from index import symbols
    symbol = input("What symbol do you want to remove: ")
    symbols.removeSymbol(symbol.upper())
    showOptions(f"symbol '{symbol.upper()}' removed")

def panic():
    if(api.panic()):
        showOptions("Panic success, all positions and orders are closed")
    else:
        showOptions("Panic failed, check 'https://alpaca.markets/' for more information")

def allSymbols():
    from index import symbols
    listOfSymbols = ""
    for symbol in symbols.listAllSymbols():
        listOfSymbols = f"{symbol.symbol},{listOfSymbols}"
    return listOfSymbols

def custom():
    from index import symbols
    print('this does whatever i need it to do')

    symbols.addSymbol('COST')
    symbols.addSymbol('ASML')
    symbols.addSymbol('TMUS')
    symbols.addSymbol('CSCO')
    symbols.addSymbol('AZN')
    symbols.addSymbol('LIN')
    symbols.addSymbol('ISRG')
    symbols.addSymbol('PEP')
    symbols.addSymbol('AMD')
    symbols.addSymbol('QCOM')
    symbols.addSymbol('ADBE')
    symbols.addSymbol('PLTR')
    symbols.addSymbol('ARM')
    symbols.addSymbol('TXN')
    symbols.addSymbol('INTU')
    symbols.addSymbol('BKNG')
    symbols.addSymbol('AMAT')
    symbols.addSymbol('AMGN')
    symbols.addSymbol('PDD')
    symbols.addSymbol('HON')
    symbols.addSymbol('CMCSA')
    symbols.addSymbol('SNY')
    symbols.addSymbol('PANW')
    symbols.addSymbol('APP')
    symbols.addSymbol('ADP')
    symbols.addSymbol('MU')
    symbols.addSymbol('GILD')
    symbols.addSymbol('VRTX')
    symbols.addSymbol('SBUX')
    symbols.addSymbol('MRVL')
    symbols.addSymbol('ADI')
    symbols.addSymbol('CEG')
    symbols.addSymbol('LRCX')
    symbols.addSymbol('KLAC')
    symbols.addSymbol('CRWD')
    symbols.addSymbol('MELI')
    symbols.addSymbol('MSTR')
    symbols.addSymbol('EQIX')
    symbols.addSymbol('INTC')
    symbols.addSymbol('PYPL')
    symbols.addSymbol('CDNS')
    symbols.addSymbol('CME')
    symbols.addSymbol('SNPS')
    symbols.addSymbol('ABNB')
    symbols.addSymbol('CTAS')
    symbols.addSymbol('MAR')
    symbols.addSymbol('MDLZ')
    symbols.addSymbol('COIN')
    symbols.addSymbol('DASH')
    symbols.addSymbol('FTNT')
    symbols.addSymbol('REGN')
    symbols.addSymbol('ORLY')
    symbols.addSymbol('TEAM')
    symbols.addSymbol('WDAY')
    symbols.addSymbol('NTES')
    symbols.addSymbol('ADSK')
    symbols.addSymbol('CSX')
    symbols.addSymbol('TTD')
    symbols.addSymbol('PCAR')
    symbols.addSymbol('JD')
    symbols.addSymbol('CHTR')
    symbols.addSymbol('ROP')
    symbols.addSymbol('CPRT')
    symbols.addSymbol('NXPI')
    symbols.addSymbol('PAYX')
    symbols.addSymbol('AEP')
    symbols.addSymbol('FANG')
    symbols.addSymbol('ROST')
    symbols.addSymbol('DDOG')
    symbols.addSymbol('LULU')
    symbols.addSymbol('AXON')
    symbols.addSymbol('MNST')
    symbols.addSymbol('NDAQ')
    symbols.addSymbol('TCOM')
    symbols.addSymbol('HOOD')
    symbols.addSymbol('BKR')
    symbols.addSymbol('FAST')
    symbols.addSymbol('KDP')
    symbols.addSymbol('ODFL')
    symbols.addSymbol('GEHC')
    symbols.addSymbol('CTSH')
    symbols.addSymbol('EXC')
    symbols.addSymbol('VRSK')
    symbols.addSymbol('ARGX')
    symbols.addSymbol('XEL')
    symbols.addSymbol('CCEP')
    symbols.addSymbol('IDXX')
    symbols.addSymbol('KHC')
    symbols.addSymbol('ALNY')
    symbols.addSymbol('ACGL')
    symbols.addSymbol('AAPL')
    symbols.addSymbol('TSLA')

    interval[0] = 15
    showOptions(clear=True)
