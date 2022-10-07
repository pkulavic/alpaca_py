from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoLatestQuoteRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

from datetime import datetime

# no keys required for crypto data
client = CryptoHistoricalDataClient()

# single symbol request
request_params = CryptoLatestQuoteRequest(symbol_or_symbols="ETH/USD")

latest_quote = client.get_crypto_latest_quote(request_params)

# must use symbol to access even though it is single symbol
latest_quote["ETH/USD"].ask_price
print(latest_quote)




class Triangle:
    """The primary function of this class is to determine if an arbitrage opportunity exists."""
    def __init__(self) -> None:
        self.client = CryptoHistoricalDataClient()
        self.api_key = 'PKPO1PBAYQWDG1BX83W1'
        self.secret_key = 'TUZDp8DncWtYVXLvliGsbfHDlmUvU9aJqenJLAbn'
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



t = Triangle()
print(t.fetch_latest_price("AVAX/USDT"))
print(t.fetch_latest_price("AVAX/BTC"))
print(1 / t.fetch_latest_price("BTC/USDT"))

print(t.compute_profit())

for asset in t.get_assets():
    if asset.tradable:
        if asset.symbol[:4] == "AVAX":
            print(asset.symbol)


