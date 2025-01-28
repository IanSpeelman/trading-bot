import cli
import utils
import threading
import time
import datetime

interval = [15]
trading = threading.Event()
trading.clear()
symbols = utils.SymbolStore()

def interface():
    if __name__ == "__main__":
        cli.showOptions()

interface()

def loop():
    run = True
    lastExecution = datetime.datetime.now(datetime.timezone.utc)
    while True:
        if not trading.is_set() and not run:
            run = True
        if not run:
            run = datetime.datetime.now(datetime.timezone.utc) > lastExecution + datetime.timedelta(minutes=interval[0])
        if trading.is_set() and run:
            if utils.checkForOpportunities(symbols):
                lastExecution = datetime.datetime.now(datetime.timezone.utc)
                run = False
            time.sleep(1)
        else:
            time.sleep(1)

threading.Thread(target=loop, daemon=True).start()
