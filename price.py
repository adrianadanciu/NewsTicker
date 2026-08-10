import yfinance as yf #library used to download the live prices
import ssl #the library responsible for security
import certifi 
try:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except AttributeError:
    pass
def get_live_price(ticker):
    """Fetches the latest available price."""
    try:
        ticker_data = yf.Ticker(ticker)
        price = ticker_data.fast_info.get("last_price")
        if price:
            return price
        #fallback for tickers where fast_info doesn't populate last_price
        history = ticker_data.history(period="1d", interval="1m")
        if not history.empty:
            return history['Close'].iloc[-1]
    except Exception as e:
        print(f" [ERROR] Failed to process live price: {e}")
    return None