# NewsTicker
Inspired by my interest in finance, I built this app to complement existing trading-prediction tools. A problem I noticed across most of them is that they rely purely on chart-based math — great at that, but missing the news and information that actually move the market. This site brings both together, helping you make informed decisions without spending hours scrolling through Facebook or other sources for news — everything is just one click away.
## Project structure
- app.py — Entry point: ties everything together
- auth.py — Login, registration, and session logic (backed by the Supabase database, not local files)
- db.py — database layer
- theme.py — All custom CSS/UI styling
- sidebar.py — Profile card, upgrade page, and configuration panel
- engine.py — Core decision logic
- results.py — Metrics, price chart, news table, and the analysis pipeline
- ai.py — FinBERT sentiment analysis
- data.py — News fetching
- price.py — Live price fetching
- payments.py — PayPal payment integration 
- legal.py — Terms of Service, Privacy Policy, and Refund Policy pages
- faq.py — Frequently Asked Questions page
## How to run it
1. Install dependencies:
pip install -r requirements.txt
2. Create `.streamlit/secrets.toml` with your own values:
toml
DB_URL = "your-supabase-postgres-connection-string"
COOKIE_KEY = "any-long-random-string"
COOKIE_NAME = "auth_cookie"
PAYPAL_CLIENT_ID = "your-paypal-client-id"
PAYPAL_CLIENT_SECRET = "your-paypal-client-secret"
APP_BASE_URL = "http://localhost:8501"
3. Run the app:
streamlit run app.py
Then open the URL shown in the terminal (usually `http://localhost:8501`).