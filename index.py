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
    if(__name__ == "__main__"):
        cli.showOptions()

interface()
# threading.Thread(target=interface).start()

def loop():
    run = True
    lastExecution = datetime.datetime.now(datetime.timezone.utc)
    # print("run", run)
    while True:
        if not trading.is_set():
            run = True
        if(not run):
            run = datetime.datetime.now(datetime.timezone.utc) > lastExecution + datetime.timedelta(minutes=interval[0])
        if trading.is_set() and run:
            lastExecution = datetime.datetime.now(datetime.timezone.utc)
            utils.checkForBets(symbols)
            run = False
            time.sleep(1)
        else:
            time.sleep(1)

loopThread = threading.Thread(target=loop, daemon=True).start()
