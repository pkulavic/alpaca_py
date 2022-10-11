from triangle import Trader, Triangle
import time


def main():
    trader = Trader()
    while True:
        if trader.triangle.compute_profit_USD("YFI") > 1.0024:
            trader.run(symbol="YFI")
        else:
            time.sleep(1)


    


if __name__ == "__main__":
    main()
