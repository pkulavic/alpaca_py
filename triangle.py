from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoLatestQuoteRequest

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
    """The primary function of this class is the arbitrage_opportunity_exists method"""
    def __init__(self) -> None:
        self.client = CryptoHistoricalDataClient()
    def arbitrage_opportunity_exists(self) -> bool:
        pass
    def fetch_latest_price(self, symbol) -> float:
        """This function returns the latest ask price of the specified token."""
        request_params = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)
        latest_quote = self.client.get_crypto_latest_quote(request_params)
        return latest_quote[symbol].ask_price

t = Triangle()
print(t.fetch_latest_price("ETH/USDT"))




