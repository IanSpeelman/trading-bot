import cli
import utils
import threading
import time

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
    while True:
        if trading.is_set():
            utils.checkForBets(symbols)
            time.sleep(interval[0] * 60)
        else:
            time.sleep(1)

loopThread = threading.Thread(target=loop, daemon=True).start()
