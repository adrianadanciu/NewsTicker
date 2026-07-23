# NewsTicker
Inspired by my interest in finance, I built this app to complement existing trading-prediction tools. A problem I noticed across most of them is that they rely purely on chart-based math — great at that, but missing the news and information that actually move the market. This site brings both together, helping you make informed decisions without spending hours scrolling through Facebook or other sources for news — everything is just one click away.
## Project structure
- **app.py** — Entry point: ties everything together 
- **auth.py** — Handles config.yaml, login, and registration
- **theme.py** — All custom CSS/UI styling
- **sidebar.py** — Profile card, upgrade page, and configuration panel
- **engine.py** — Core decision logi
- **dashboard.py** — Metrics, price chart, news table and the analysis pipeline
- **ai.py** — FinBERT sentiment analysis
- **data.py** — News fetching 
- **trading.py** — Live price fetching
- **config.yaml** — User accounts and settings
## How to run it
pip install -r requirements.txt
python3 -m streamlit run app.py --server.headless true
Then open the URL shown in the terminal (usually `http://localhost:8501`).