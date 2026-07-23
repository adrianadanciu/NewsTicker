import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import data
import ai
import price
import engine
#the app has a search memory of 10 minutes
@st.cache_data(ttl=600, show_spinner=False)
def cached_fetch_price_history(ticker, period, interval="1d"):
    try:
        history = yf.download(ticker, period=period, interval=interval, progress=False)
        if history is None or history.empty:
            return None
        return history
    except Exception:
        return None
def _flatten_ohlc(df):
    #yfinance sometimes returns a MultiIndex for the columns, this collapses it back down
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close"]]
@st.cache_data(ttl=600, show_spinner=False) #this line appears twice because it only has effect on one function at a time
def cached_fetch_data(ticker, plan):
    if plan == "Free":
        news = data.fetch_google_news(ticker)
        news = [n for n in news if n.get("source") != "Ticker Nerd"]
        return news
    else:
        news = data.fetch_google_news(ticker)
        reddit = data.fetch_reddit_wsb(ticker)
        return news + reddit
def restore_last_analysis(user_data):
    """Restores the last saved analysis."""
    if "restored_last_analysis" in st.session_state:
        return
    st.session_state.restored_last_analysis = True
    last_analysis = user_data.get('last_analysis')
    if last_analysis and last_analysis.get('headlines'):
        st.session_state.all_headlines = last_analysis.get('headlines', [])
        st.session_state.current_price = last_analysis.get('current_price')
        stats = last_analysis.get('ai_stats')
        if stats:
            st.session_state.ai_stats = tuple(stats)
        st.session_state.active_ticker = last_analysis.get('ticker', '')
        st.session_state.operation_mode = last_analysis.get('option', 'BUY')
        st.session_state.analysis_done = True
def run_analysis_pipeline(target_company, option, user_plan, user_usage, config, current_username, save_config):
    """Fetches news, runs the AI sentiment analysis, fetches the live price and redirects everything to the session state."""
    with st.spinner(""): #fetches the news
        all_headlines = cached_fetch_data(target_company, user_plan)
    if not all_headlines:
        st.error(f"No headlines found for '{target_company}'.")
        return
    with st.spinner(""):
        pos, neg, neut, dilution, growth, enriched_headlines = ai.analyze_headlines(all_headlines)
    current_price = price.get_live_price(target_company)
    st.session_state.all_headlines = enriched_headlines
    st.session_state.current_price = current_price
    st.session_state.ai_stats = (pos, neg, neut, dilution, growth)
    st.session_state.active_ticker = target_company
    st.session_state.analysis_done = True
    config['credentials']['usernames'][current_username]['last_ticker'] = target_company
    config['credentials']['usernames'][current_username]['last_analysis'] = {
        'ticker': target_company,
        'option': option,
        'current_price': float(current_price) if current_price is not None else None,
        'ai_stats': [pos, neg, neut, dilution, growth],
        'headlines': enriched_headlines,
    }
    if user_plan == "Free":
        user_usage['count'] += 1
        config['credentials']['usernames'][current_username]['usage'] = user_usage
    save_config(config)
    #only Free needs an immediate rerun here, so the "X out of 3 analyses left" banner updates right away; Premium has no counter to refresh.
    if user_plan == "Free":
        st.rerun()
def render_intro_card(target_company, option, user_plan):
    st.markdown(f"""
    <div class="premium-card" style="border-left: 4px solid #00f2fe; margin-top: 15px; margin-bottom: 25px;">
        <p style="color: #cbd5e1; font-size: 1.25rem; line-height: 1.6; margin: 0;">
            Select the operational parameters in the left control panel and click <b>Run analysis</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    intro_col1, intro_col2, intro_col3 = st.columns(3, gap="medium")
    intro_col1.metric("Selected Ticker", target_company)
    intro_col2.metric("Operation Mode", option)
    intro_col3.metric("Account Tier", user_plan)
def _render_buy_card(rec):
    html = f"""
    <div class="premium-card" style="border-left: 4px solid {rec['border_color']};">
        <h2 style="color: {rec['text_color']}; margin-top: 0; margin-bottom: 12px; font-weight: 800; font-size: 1.4rem;">{rec['title']}</h2>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; margin: 0;">{rec['explanation']}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
def _render_sell_card(rec):
    html = f"""
    <div class="premium-card" style="border-left: 4px solid {rec['border_color']};">
        <h2 style="color: #ffffff; margin-top: 0; margin-bottom: 12px;">{rec['title']}</h2>
        <p style="color: #cbd5e1;">{rec['explanation']}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
TIMEFRAME_CONFIG = {
    "1H": {"interval": "60m", "period": "5d"},
    "4H": {"interval": "60m", "period": "60d", "resample": "4h"},
    "Weekly": {"interval": "1wk", "period": "5y"},
    "1mo": {"interval": "1d", "period": "1mo"},
    "3mo": {"interval": "1d", "period": "3mo"},
    "6mo": {"interval": "1d", "period": "6mo"},
    "1y": {"interval": "1d", "period": "1y"},
}
def render_price_chart(target_company):
    st.write("---")
    st.subheader("Price Trend")
    timeframe = st.radio(
        "Timeframe", list(TIMEFRAME_CONFIG.keys()),
        index=4, horizontal=True, label_visibility="collapsed"
    )
    cfg = TIMEFRAME_CONFIG[timeframe]
    price_history = cached_fetch_price_history(target_company, cfg["period"], cfg["interval"])
    if price_history is not None:
        ohlc = _flatten_ohlc(price_history)
        if "resample" in cfg:
            ohlc = ohlc.resample(cfg["resample"]).agg({
                "Open": "first", "High": "max", "Low": "min", "Close": "last",
            }).dropna()
        if ohlc.empty:
            st.info("Not enough intraday history is available for this timeframe.")
            return
        if len(ohlc) < 5:
            st.warning(
                f"⚠ Only {len(ohlc)} bar(s) of trading history available for {target_company} "
                f"The chart below may look misleading with so little data."
            )
        if cfg["interval"] == "60m":
            x_labels = ohlc.index.strftime("%b %d, %H:%M")
        else:
            x_labels = ohlc.index.strftime("%b %d, %Y")

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=x_labels,
            open=ohlc["Open"],
            high=ohlc["High"],
            low=ohlc["Low"],
            close=ohlc["Close"],
            increasing_line_color="#39ff6a",
            increasing_fillcolor="#39ff6a",
            decreasing_line_color="#ff4b4b",
            decreasing_fillcolor="#ff4b4b",
            name=target_company,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Open: %{open:.2f}<br>"
                "High: %{high:.2f}<br>"
                "Low: %{low:.2f}<br>"
                "Close: %{close:.2f}"
                "<extra></extra>"
            ),
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
            font=dict(color="#cbd5e1"),
            # type="category" plots bars back-to-back in sequence instead of on a real calendar time axis, so nights/weekends with no trading don't show up as big empty gaps that squeeze the actual candles into a tiny cluster.
            xaxis=dict(showgrid=False, rangeslider=dict(visible=False), type="category", nticks=10),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Price history is not available for this ticker.")
def render_news_table(all_headlines):
    st.write("---")
    st.subheader("News Analysis & Classification")
    html_table = """
    <style>
        .premium-table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95rem; background-color: #0b0d1a; }
        .premium-table th { background-color: #12162e; color: #637099; text-align: left; padding: 12px 16px; font-weight: 600; border-bottom: 2px solid #1f2647; text-transform: uppercase; font-size: 0.8rem; }
        .premium-table td { padding: 14px 16px; border-bottom: 1px solid #1f2647; color: #cbd5e1; }
        .premium-table tr:hover { background-color: #161b38; transition: background-color 0.2s ease; }
        .headline-link { color: #1f77b4 !important; text-decoration: none !important; }
        .headline-link:hover { color: #00f2fe !important; }
        .badge-source { background-color: #12162e; color: #f0f2f6; padding: 6px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid #232c5c; }
        .sentiment-symbol { font-size: 1.1rem; font-weight: 700; }
    </style>
    <table class="premium-table"><thead><tr>
        <th style="width: 8%; text-align: center;">Sentiment</th>
        <th style="width: 22%;">Publisher</th>
        <th style="width: 70%;">Headline</th>
    </tr></thead><tbody>
    """
    sentiment_display = {
        "POSITIVE": ("▲", "#39ff6a", "Positive"),
        "NEGATIVE": ("▼", "#ff4b4b", "Negative"),
        "NEUTRAL": ("●", "#8a90a6", "Neutral"),
    }
    for item in all_headlines:
        source = item["source"]
        text = item["text"].replace('"', '&quot;').replace("'", "&#39;")
        link = item["link"]
        symbol, color, label = sentiment_display.get(item.get("sentiment"), ("●", "#8a90a6", "Unknown"))
        confidence = item.get("confidence")
        title_attr = f'{label} ({confidence:.0f}% confidence)' if confidence is not None else label
        sentiment_html = f'<span class="sentiment-symbol" style="color: {color};" title="{title_attr}">{symbol}</span>'
        html_table += (
            f'<tr><td style="text-align: center;">{sentiment_html}</td>'
            f'<td><span class="badge-source">{source}</span></td>'
            f'<td><a class="headline-link" href="{link}" target="_blank">{text} ↗</a></td></tr>'
        )
    html_table += "</tbody></table>"
    st.html(html_table)
def render_dashboard(target_company, option, user_plan, confidence_threshold):
    """Renders the full dashboard: metrics, recommendation card, price chart, news table."""
    all_headlines = st.session_state.all_headlines
    current_price = st.session_state.current_price
    pos, neg, neut, dilution, growth = st.session_state.ai_stats
    directional_opinions, have_enough_sample, bullish_pct_value, sample_note, min_required = (
        engine.compute_sentiment_stats(pos, neg, neut)
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if current_price:
            currency, _ = engine.get_currency(target_company)
            st.metric(label="Live Spot Price", value=f"{current_price:.2f} {currency}")
        else:
            st.metric(label="Live Spot Price", value="Offline / Delisted")
    with col2:
        if bullish_pct_value is not None:
            low_sample_help = (
                "Based on fewer than 5 directional headlines — this percentage "
                "isn't statistically reliable yet. Treat it with caution."
                if not have_enough_sample else None
            )
            sentiment_label = "Bullish" if bullish_pct_value >= 50 else "Bearish"
            st.metric(
                label="Net AI Sentiment",
                value=f"{bullish_pct_value:.1f}% {sentiment_label}",
                help=low_sample_help,
            )
        else:
            st.metric(label="Net AI Sentiment", value="No Directional Data")
    with col3:
        st.metric(label="Neutral Noise Filtered", value=f"{neut} Articles")
    st.write("---")
    st.subheader("Executive order")
    tech_history = cached_fetch_price_history(target_company, "3mo")
    technical_bullish, tech_note = engine.compute_technical_trend(tech_history)
    atr_pct = engine.compute_atr_percent(tech_history)
    if option == "BUY":
        rec = engine.build_buy_recommendation(
            dilution, growth, have_enough_sample, bullish_pct_value, confidence_threshold,
            technical_bullish, tech_note, sample_note, current_price, target_company,
            atr_pct=atr_pct,
        )
        _render_buy_card(rec)
    elif option == "SELL":
        st.markdown("#### Input portfolio specifications:")
        with st.form("portfolio_form"):
            entry_price = st.number_input("At what price did you buy?", min_value=0.01, value=None, placeholder="e.g. 150.00")
            shares_count = st.number_input("How many units?", min_value=0.1, value=None, placeholder="e.g. 10")
            submit_portfolio = st.form_submit_button("Calculate exit")
        if submit_portfolio:
            if entry_price is None or shares_count is None:
                st.warning("Please fill in both fields before calculating.")
                st.stop()
            invested_value = entry_price * shares_count
            if current_price:
                gross_profit = (current_price * shares_count) - invested_value
                percent_diff = ((current_price - entry_price) / entry_price) * 100
                is_profitable = current_price > entry_price
                st.subheader("Current portfolio balance")
                p_col1, p_col2 = st.columns(2)
                p_col1.metric("Return percentage", f"{percent_diff:+.2f}%")
                p_col2.metric("Profit/Loss Amount", f"{gross_profit:+.2f}")
                st.write("---")
                bullish_pct = bullish_pct_value if bullish_pct_value is not None else 50.0
                rec = engine.build_sell_recommendation(
                    is_profitable, dilution, growth, have_enough_sample, bullish_pct,
                    confidence_threshold, technical_bullish, tech_note, sample_note,
                )
                _render_sell_card(rec)
    render_price_chart(target_company)
    render_news_table(all_headlines)