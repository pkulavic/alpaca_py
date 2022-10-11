from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoLatestQuoteRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderStatus

from alpaca.trading.requests import GetOrdersRequest

from alpaca.trading.enums import QueryOrderStatus

from alpaca.trading.models import Order

from colorama import Fore

import apikey
import time

class Triangle:
    """The primary function of this class is to determine if an arbitrage opportunity exists."""
    def __init__(self) -> None:
        self.data_client = CryptoHistoricalDataClient()
        self.api_key = apikey.apikey
        self.secret_key = apikey.secret_key
        self.tradable_assets = self.get_list_of_tradable_assets()
        self.trading_client = TradingClient(self.api_key, self.secret_key, paper=True)
    def arbitrage_opportunity_exists(self) -> bool:
        pass
    def fetch_latest_ask(self, symbol) -> float:
        """This function returns the latest ask price of the specified token."""
        request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)
        latest_quote = self.data_client.get_crypto_latest_quote(request_params)
        return latest_quote[symbol].ask_price
    def fetch_latest_bid(self, symbol) -> float:
        """This function returns the latest bid price of the specified token."""
        request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)
        latest_quote = self.data_client.get_crypto_latest_quote(request_params)
        return latest_quote[symbol].bid_price
    def compute_profit(self, symbol: str):
        try:
            return self.fetch_latest_ask("BTC/USDT") * \
                self.fetch_latest_ask(symbol + "/BTC") * \
                (1 / self.fetch_latest_ask(symbol + "/USDT")) # bid
        except KeyError as e:
            raise KeyError(str(e))
    def compute_profit_USD(self, symbol: str):
        try:
            return self.fetch_latest_ask("BTC/USD") * \
                self.fetch_latest_ask(symbol + "/BTC") * \
                (1 / self.fetch_latest_ask(symbol + "/USD"))
        except KeyError as e:
            raise KeyError(str(e))
    def get_assets(self):
        trading_client = TradingClient(self.api_key, self.secret_key)
        search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)
        assets = trading_client.get_all_assets(search_params)
        return assets
    def get_list_of_tradable_assets(self):
        assets = self.get_assets()
        tradable_assets = []
        for asset in assets:
            if asset.tradable:
                # Only look at tokens that can be traded for BTC
                if "BTC" in asset.symbol and "BTC" != asset.symbol[:3]:
                    # Get only the part before the slash
                    tradable_assets.append(asset.symbol.split('/')[0])
        return tradable_assets
    def place_order(self, token, amount):
        pass


class Trader:
    """This class' job is to perform trades."""
    DEFAULT_AMOUNT_USD: float = 10000.00 # $10,000
    def __init__(self) -> None:
        super().__init__()
        self.triangle = Triangle()
    def run(self, symbol) -> None:
        """This function monitors market prices. If it notices a profitable opportunity, 
        it executes a trade."""
        # Liquidates all open positions beforehand
        # self.triangle.trading_client.close_all_positions(True)
        print(self.execute_triangle_trade(symbol=symbol))
    def execute_triangle_trade(self, symbol: str, amount=DEFAULT_AMOUNT_USD) -> None: #returns an order
        order1 = LimitOrderRequest(
            symbol="BTC/USD",
            limit_price=self.triangle.fetch_latest_ask("BTC/USD"),
            notional=amount,
            side=OrderSide.BUY,
            time_in_force = TimeInForce.GTC
        )
        order1_response = self.triangle.trading_client.submit_order(order_data=order1)
        
        while self.get_latest_closed_order().id != order1_response.id:
            time.sleep(0.5)
            print("Waiting for order 1 to be filled")
        print("Order 1 filled")
        print(order1_response.id)

        order2 = LimitOrderRequest(
            symbol=f"{symbol}/BTC",
            limit_price=self.triangle.fetch_latest_ask(f"{symbol}/BTC"),
            notional=float(self.triangle.trading_client.get_open_position('BTCUSD').qty),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        order2_response = self.triangle.trading_client.submit_order(order_data=order2)
        while self.get_latest_closed_order().id != order2_response.id:
            time.sleep(0.5)
            print("Waiting for order 2 to be filled")
        print("Order 2 filled")
        print(order2_response.id)
        
        order3 = LimitOrderRequest(
            symbol=f"{symbol}/USD",
            limit_price=self.triangle.fetch_latest_bid(f"{symbol}/USD"),
            qty=(float(self.triangle.trading_client.get_open_position(f"{symbol}USD").qty) // .001 / 1000),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        print(order3.qty)
        order3_response = self.triangle.trading_client.submit_order(order_data=order3)

        while self.get_latest_closed_order().id != order3_response.id:
            time.sleep(0.5)
            print("Waiting for order 3 to be filled")
        print("Order 3 filled")
        print(order3_response.id)

        return order3_response
    
    def get_all_orders(self):
        orders_request = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED
        )
        return self.triangle.trading_client.get_orders(filter=orders_request)
    def get_order_by_id(self, id):
        order_request = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED
        )
        orders = self.triangle.trading_client.get_orders(filter=order_request)
        for order in orders:
            if order.id == id:
                return order
    def get_latest_closed_order(self) -> Order:
        return self.get_all_orders()[0]
    
    def get_balance_by_token(self, symbol):
        return self.triangle.trading_client.get_open_position(symbol)

    def get_open_position(self, symbol):
        pass









def main():
    t = Triangle()
    print(t.tradable_assets)
    # USDT = base currency
    for asset in t.tradable_assets:
        try: 
            profit = t.compute_profit(asset)
        except KeyError:
            pass
        else:
            if profit > 1.0024:
                print(asset + ": " + Fore.GREEN + str(profit) + Fore.WHITE)
            else:
                print(asset + ": " + Fore.RED + str(profit) + Fore.WHITE)
    # USD = base currency
    for asset in t.tradable_assets:
        try: 
            profit = t.compute_profit_USD(asset)
        except KeyError:
            pass
        else:
            if profit > 1.0024:
                print(asset + "/USD: " + Fore.GREEN + str(profit) + Fore.WHITE)
            else:
                print(asset + "/USD: " + Fore.RED + str(profit) + Fore.WHITE)
            



if __name__ == "__main__":
    main()



