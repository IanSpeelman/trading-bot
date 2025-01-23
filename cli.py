import os
import api
from index import interval
from index import trading
from index import loopThread

def showOptions(msg="", clear=True):
    if(clear):
        os.system("clear")

    print(msg)
    print('1) Start Trading')
    print('2) Stop Trading')
    print('3) Change interval')
    print('4) Add symbol')
    print('5) Remove symbol')
    print('q) Quit')
    print("====================== settings ======================")
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

def allSymbols():
    from index import symbols
    listOfSymbols = ""
    for symbol in symbols.listAllSymbols():
        listOfSymbols = f"{symbol.symbol},{listOfSymbols}"
    return listOfSymbols

def custom():
    from index import symbols
    print('this does whatever i need it to do')
    symbols.addSymbol("AAPL")
    symbols.addSymbol("meta")
    symbols.addSymbol("xom")
    symbols.addSymbol("msft")
    symbols.addSymbol("bp")
    symbols.addSymbol("jnj")
    symbols.addSymbol("jpm")
    symbols.addSymbol("ubs")
    symbols.addSymbol("t")
    symbols.addSymbol("pep")
    symbols.addSymbol("pfe")
    interval[0] = 1
    showOptions(clear=True)
