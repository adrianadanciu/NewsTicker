import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#hl = host language, gl = gelocation, ceid = custom search id
MARKETS_DATABASE = {
    "US": {"hl": "en-US", "gl": "US", "ceid": "US:en", "term": "stock news"},
    "CA": {"hl": "en-CA", "gl": "CA", "ceid": "CA:en", "term": "stock news"}, 
    "MX": {"hl": "es-419", "gl": "MX", "ceid": "MX:es", "term": "bolsa de valores"},
    "BR": {"hl": "pt-BR", "gl": "BR", "ceid": "BR:pt", "term": "ações bolsa"},
    "AR": {"hl": "es-419", "gl": "AR", "ceid": "AR:es", "term": "acciones bolsa"},
    "RO": {"hl": "ro", "gl": "RO", "ceid": "RO:ro", "term": "bursa actiuni"}, 
    "UK": {"hl": "en-GB", "gl": "GB", "ceid": "GB:en", "term": "stock shares"}, 
    "DE": {"hl": "de", "gl": "DE", "ceid": "DE:de", "term": "aktien börse"}, 
    "FR": {"hl": "fr", "gl": "FR", "ceid": "FR:fr", "term": "actions bourse"},
    "IT": {"hl": "it", "gl": "IT", "ceid": "IT:it", "term": "azioni borsa"},
    "ES": {"hl": "es", "gl": "ES", "ceid": "ES:es", "term": "acciones bolsa"},
    "NL": {"hl": "nl", "gl": "NL", "ceid": "NL:nl", "term": "aandelen beurs"},
    "BE": {"hl": "fr-BE", "gl": "BE", "ceid": "BE:fr", "term": "actions bourse"}, 
    "CH": {"hl": "de-CH", "gl": "CH", "ceid": "CH:de", "term": "aktien börse"},
    "SE": {"hl": "sv", "gl": "SE", "ceid": "SE:sv", "term": "aktier börsen"},
    "NO": {"hl": "no", "gl": "NO", "ceid": "NO:no", "term": "aksjer børs"}, 
    "DK": {"hl": "da", "gl": "DK", "ceid": "DK:da", "term": "aktier børsen"}, 
    "PL": {"hl": "pl", "gl": "PL", "ceid": "PL:pl", "term": "akcje giełda"},
    "JP": {"hl": "ja", "gl": "JP", "ceid": "JP:ja", "term": "株価 ニュース"},
    "CN": {"hl": "zh-CN", "gl": "CN", "ceid": "CN:zh", "term": "股票 新闻"}, 
    "HK": {"hl": "zh-HK", "gl": "HK", "ceid": "HK:zh", "term": "股票 報價"},
    "IN": {"hl": "en-IN", "gl": "IN", "ceid": "IN:en", "term": "share market"}, 
    "AU": {"hl": "en-AU", "gl": "AU", "ceid": "AU:en", "term": "shares news"}, 
    "KR": {"hl": "ko", "gl": "KR", "ceid": "KR:ko", "term": "주식 뉴스"},
    "SG": {"hl": "en-SG", "gl": "SG", "ceid": "SG:en", "term": "stocks trading"},
    "ZA": {"hl": "en-ZA", "gl": "ZA", "ceid": "ZA:en", "term": "shares market"}, 
    "IL": {"hl": "he", "gl": "IL", "ceid": "IL:he", "term": "מניות בורסה"}, 
    "SA": {"hl": "ar", "gl": "SA", "ceid": "SA:ar", "term": "أسهم تداول"},
}
#Google News blocheaza/raspunde diferit cererilor fara un User-Agent de browser
#real -- fara asta, cererile facute din adrese IP de tip cloud/server (cum e
#Streamlit Cloud) pot fi respinse sau golite silentios, in timp ce local, de
#pe conexiunea obisnuita de acasa, functioneaza fara probleme.
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
def fetch_google_news(ticker):
    """First source of news and headlines from which the app takes its data throughout Google News"""
    headlines = []
    seen_titles = set()#a new set
    suffix = "US"
    clean_ticker = ticker
    if "." in ticker:
        possible_suffix = ticker.split(".")[-1].upper()
        if possible_suffix in MARKETS_DATABASE:
            suffix = possible_suffix
            clean_ticker = ticker.split(".")[0]
    config = MARKETS_DATABASE.get(suffix, MARKETS_DATABASE["US"])
    hl = config["hl"]
    gl = config["gl"]
    ceid = config["ceid"]
    local_term = config["term"]
    search_query = f'"{clean_ticker}" OR "{clean_ticker} {local_term}"'
    url = f"https://news.google.com/rss/search?q={search_query}&hl={hl}&gl={gl}&ceid={ceid}"
    urls = [url]
    #extended history lookback, since Google News favors very recent articles by default
    lookback_date = (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d")
    extended_query = f'{search_query} after:{lookback_date}'
    extended_url = f"https://news.google.com/rss/search?q={extended_query}&hl={hl}&gl={gl}&ceid={ceid}"
    urls.append(extended_url)
    #for the american market there are listed a few trustworthy news outlets
    if suffix == "US":
        premium_outlets = [
            "Fox News", "Yahoo Finance", "The Street", "CNBC", "Fossbytes",
            "CryptosRUs", "Ash Crypto", "The Cryptology Academy", "Finviz", "Ticker Nerd"
        ]
        outlets_query = " OR ".join([f'"{source}"' for source in premium_outlets])
        #for smaller platforms the search using the "site method" was added
        query_premium = f'{ticker} AND ({outlets_query} OR site:finviz.com OR site:thestreet.com OR site:tickernerd.com)'
        urls = [
            f"https://news.google.com/rss/search?q={query_premium}&hl=en-US&gl=US&ceid=US:en",
            url,
            extended_url,
        ]
    for target_url in urls:
        try:
            response = requests.get(target_url, headers=REQUEST_HEADERS, timeout=10)
            print(f"[DEBUG] URL: {target_url[:100]}... | status={response.status_code} | body_len={len(response.text)}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')
                print(f"[DEBUG] Parsed {len(items)} <item> elements from this response.")
                for item in items:
                    if len(headlines) >= 75:
                        break
                    if item.title:
                        title_text = item.title.text
                        if title_text.lower() in seen_titles: #eliminates the duplicates
                            continue
                        seen_titles.add(title_text.lower())
                        article_link = item.link.text if item.link else "https://news.google.com" #creates a fallback in case the link doesn't exist
                        detected_source = item.source.text if item.source else "Financial Press"
                        #showing a more beautiful showcase for important american news
                        if suffix == "US":
                            source_raw = detected_source.lower()
                            link_raw = article_link.lower()
                            title_lower = title_text.lower()
                            if "tickernerd" in source_raw or "ticker nerd" in title_lower or "tickernerd" in link_raw:
                                detected_source = "Ticker Nerd"
                            elif "thestreet" in source_raw or "the street" in title_lower or "thestreet" in link_raw:
                                detected_source = "The Street"
                            elif "cnbc" in source_raw or "cnbc" in title_lower or "cnbc" in link_raw:
                                detected_source = "CNBC"
                            elif "yahoo" in source_raw or "yahoo finance" in title_lower or "yahoo" in link_raw:
                                detected_source = "Yahoo Finance"
                            elif "finviz" in source_raw or "finviz" in title_lower or "finviz" in link_raw:
                                detected_source = "Finviz"
                        headlines.append({
                            "source": detected_source, 
                            "text": title_text,
                            "link": article_link
                        })
        except Exception as e:
            print(f"[ERROR] Failed to process news data: {e}")
    return headlines
def fetch_reddit_wsb(ticker):
    """First source of news and headlines from which the app takes its data throughout Reddits's subreddit WallStreetBets"""
    headlines = []
    if "." in ticker:
        return headlines #reddit is used only for the us market
    search_query = f'site:reddit.com/r/wallstreetbets "{ticker}"'
    url = f"https://news.google.com/rss/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')
            for item in items[:20]:
                if item.title:
                    title_text = item.title.text
                    clean_title = title_text.split(" - r/")[0].split(" - Reddit")[0]
                    article_link = item.link.text if item.link else "https://reddit.com/r/wallstreetbets"
                    headlines.append({
                        "source": "Reddit (r/wsb)", 
                        "text": clean_title,
                        "link": article_link
                    })
    except Exception:
        pass #as it's not our main source of data, we don't need log noise
    return headlines