import pandas as pd #data processing

#currency dictionary
CURRENCY_BY_SUFFIX = {
    "RO": ("RON", None),
    "DE": ("EUR", "€"), "FR": ("EUR", "€"), "IT": ("EUR", "€"), "ES": ("EUR", "€"),
    "NL": ("EUR", "€"), "BE": ("EUR", "€"),
    "UK": ("GBP", "£"),
    "JP": ("JPY", "¥"), "CN": ("CNY", "¥"),
    "HK": ("HKD", "HK$"),
    "IN": ("INR", "₹"),
    "AU": ("AUD", "A$"),
    "KR": ("KRW", "₩"),
    "SG": ("SGD", "S$"),
    "ZA": ("ZAR", "R"),
    "IL": ("ILS", "₪"),
    "CA": ("CAD", "C$"),
    "MX": ("MXN", "$"),
    "BR": ("BRL", "R$"),
    "AR": ("ARS", "$"),
    "CH": ("CHF", None),
    "SE": ("SEK", None),
    "NO": ("NOK", None),
    "DK": ("DKK", None),
    "PL": ("PLN", None),
    "SA": ("SAR", None),
}
DEFAULT_CURRENCY = ("USD", "$")#US market is the system default
def get_currency(target_company):
    if "." in target_company:
        suffix = target_company.split(".")[-1].upper()
        if suffix in CURRENCY_BY_SUFFIX:
            return CURRENCY_BY_SUFFIX[suffix]
    return DEFAULT_CURRENCY
def format_price(value, target_company):
    code, symbol = get_currency(target_company)
    if symbol:
        return f"{symbol}{value:.2f}"
    return f"{value:.2f} {code}"
def compute_technical_trend(price_history):
    """Calculates historical trend based on the chart."""
    technical_bullish = None
    if price_history is not None and len(price_history) >= 20:
        #extracting the close price
        if isinstance(price_history.columns, pd.MultiIndex):
            close = price_history["Close"].iloc[:, 0]
        else:
            close = price_history["Close"]
        sma20 = close.rolling(window=20).mean()
        technical_bullish = bool(close.iloc[-1] > sma20.iloc[-1])
    if technical_bullish is True:
        tech_note = "Chart trend: price is above its 20-day average (uptrend)."
    elif technical_bullish is False:
        tech_note = "Chart trend: price is below its 20-day average (downtrend)."
    else:
        tech_note = "Chart trend: not enough price history to confirm a trend."
    return technical_bullish, tech_note
def compute_atr_percent(price_history, period=14):
    """Calculates the volatility of an action per day."""
    if price_history is None or len(price_history) < period + 1:
        return None
    if isinstance(price_history.columns, pd.MultiIndex):
        high = price_history["High"].iloc[:, 0]
        low = price_history["Low"].iloc[:, 0]
        close = price_history["Close"].iloc[:, 0]
    else:
        high = price_history["High"]
        low = price_history["Low"]
        close = price_history["Close"]
    prev_close = close.shift(1)
    true_range = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean().iloc[-1]
    current = close.iloc[-1]
    if not current:
        return None
    return (atr / current) * 100
def _pullback_fraction(atr_pct):
    """Verifies the existence of the volatility average"""
    if atr_pct is None:
        return 0.075 #safety net
    return atr_pct / 100
MIN_DIRECTIONAL_SAMPLE = 5  #baseline for well-covered tickers
def _required_directional_sample(total_analyzed):
    """Adapts the minimum directional-headline bar to how much news coverage a ticker actually has."""
    if total_analyzed < 6:
        return 1
    if total_analyzed < 12:
        return 2
    if total_analyzed < 20:
        return 3
    return MIN_DIRECTIONAL_SAMPLE
def compute_sentiment_stats(pos, neg, neut):
    """Returns variables for buy/sell strategies."""
    directional_opinions = pos + neg
    total_analyzed = directional_opinions + neut
    min_required = _required_directional_sample(total_analyzed)
    #true/false variable
    have_enough_sample = directional_opinions >= min_required
    bullish_pct_value = (pos / directional_opinions) * 100 if directional_opinions > 0 else None
    sample_note = f"Based on {directional_opinions} directional headline(s) out of {total_analyzed} analyzed."
    return directional_opinions, have_enough_sample, bullish_pct_value, sample_note, min_required
def build_buy_recommendation(dilution, growth, have_enough_sample, bullish_pct_value, confidence_threshold, technical_bullish, tech_note, sample_note, current_price, target_company, atr_pct=None):
    sentiment_bullish = growth or (bullish_pct_value is not None and bullish_pct_value >= confidence_threshold)
    warning = "" if have_enough_sample else f"<br><br>⚠ <i>{sample_note} Treat this signal with extra caution.</i>"
    if dilution:
        return {
            "title": "WAIT FOR DROP",
            "explanation": f"The price may move in a misleading direction for a short while before a real drop. It's safer to wait until things settle down before buying.<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#ff4b4b",
            "text_color": "#ff4b4b",
        }
    if sentiment_bullish and technical_bullish is False:
        return {
            "title": "WAIT FOR STABLIZATION",
            "explanation": f"Sentiment is bullish, but the chart shows a downtrend. It's safer to wait until the price moves back above its 20-day average before buying.<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#f39c12",
            "text_color": "#f39c12",
        }
    if sentiment_bullish:
        border_color = "#00f2fe"
        text_color = "#ffffff"
        if current_price:
            deep_pullback = current_price * _pullback_fraction(atr_pct)
            target_entry_price = current_price - deep_pullback
            invalidation_price = target_entry_price * (1 - _pullback_fraction(atr_pct))
            confirmation = "Confirmed by a technical uptrend." if technical_bullish else "Not enough price history to confirm the trend yet."
            explanation = (
                f"Strongly bullish sentiment. {confirmation}<br><br>"
                f"<b>Optimal entry limit price:</b> {format_price(target_entry_price, target_company)}<br>"
                f"<b>Invalidation Stop Loss:</b> {format_price(invalidation_price, target_company)}{warning}"
            )
        else:
            explanation = f"Bullish sentiment. Price offline.<br><br><i>{tech_note}</i>{warning}"
        return {
            "title": "BUY NOW",
            "explanation": explanation,
            "border_color": border_color,
            "text_color": text_color,
        }
    if technical_bullish is True:
        return {
            "title": "WATCH — PRICE LOOKS GOOD, NEWS ISN'T CONVINCING YET",
            "explanation": f"The chart shows an uptrend, but news sentiment doesn't yet support a full entry. Monitor for confirmation.<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#f39c12",
            "text_color": "#f39c12",
        }
    return {
        "title": "STAY NEUTRAL",
        "explanation": f"Insufficient buying pressure.<br><br><i>{tech_note}</i>{warning}",
        "border_color": "#f39c12",
        "text_color": "#f39c12",
    }
def build_sell_recommendation(is_profitable, dilution, growth, have_enough_sample, bullish_pct, confidence_threshold, technical_bullish, tech_note, sample_note):
    warning = "" if have_enough_sample else f"<br><br>⚠ <i>{sample_note} Treat this signal with extra caution.</i>"
    if is_profitable and dilution:
        return {
            "title": "IMMEDIATE MARKET EXIT",
            "explanation": f"Secure profit now — signs point to insider selling and the price could drop soon.<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#ff4b4b",
        }
    if is_profitable and technical_bullish is False:
        return {
            "title": "TECHNICAL EXIT SIGNAL",
            "explanation": f"Price has broken below its 20-day average.<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#ff4b4b",
        }
    if is_profitable and (bullish_pct >= confidence_threshold or growth) and technical_bullish is not False:
        confirmation = " Confirmed by a technical uptrend." if technical_bullish else ""
        return {
            "title": "HOLD YOUR INVESTMENTS",
            "explanation": f"Momentum still looks strong. Move your stop-loss up as the price rises to lock in gains.{confirmation}<br><br><i>{tech_note}</i>{warning}",
            "border_color": "#00f2fe",
        }
    return {
        "title": "MAINTAIN CURRENT POSITION",
        "explanation": f"No strong signal to exit yet.<br><br><i>{tech_note}</i>{warning}",
        "border_color": "#cbd5e1",
    }