from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoLatestQuoteRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

from datetime import datetime


class Triangle:
    """The primary function of this class is to determine if an arbitrage opportunity exists."""
    def __init__(self) -> None:
        self.client = CryptoHistoricalDataClient()
        self.api_key = 'PKPO1PBAYQWDG1BX83W1'
        self.secret_key = 'TUZDp8DncWtYVXLvliGsbfHDlmUvU9aJqenJLAbn'
        self.tradable_assets = self.get_list_of_tradable_assets()
    def arbitrage_opportunity_exists(self) -> bool:
        pass
    def fetch_latest_price(self, symbol) -> float:
        """This function returns the latest ask price of the specified token."""
        request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)
        latest_quote = self.client.get_crypto_latest_quote(request_params)
        return latest_quote[symbol].ask_price
    def compute_profit(self):
        return self.fetch_latest_price("BTC/USDT") * \
            self.fetch_latest_price("ETH/BTC") * \
            (1 / self.fetch_latest_price("ETH/USDT"))
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



def main():
    t = Triangle()
    print(t.fetch_latest_price("AVAX/USDT"))
    print(t.fetch_latest_price("AVAX/BTC"))
    print(1 / t.fetch_latest_price("BTC/USDT"))

    print(t.compute_profit())

    print(t.tradable_assets)



if __name__ == "__main__":
    main()



