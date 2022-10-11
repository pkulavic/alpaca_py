from triangle import Trader



def main():
    trader = Trader()
    trader.run()
    print(trader.get_all_orders()[0])


if __name__ == "__main__":
    main()
