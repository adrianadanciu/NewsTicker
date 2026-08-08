"""Page of frequently asked questions."""
import streamlit as st
FAQ_SECTIONS = [
    {
        "category": "Getting Started",
        "items": [
            (
                "What is NewsTicker?",
                "NewsTicker scans live financial news headlines for a ticker you choose, runs AI sentiment"
                "analysis on them (using FinBERT, a model trained specifically on financial text), "
                "cross-checks that sentiment against recent price trends and gives you a single, clear "
                "read on the market instead of you having to scroll through dozens of articles yourself.",
            ),
            (
                "How do I run my first analysis?",
                "Log in, pick **BUY** or **SELL** mode in the sidebar, type a company ticker (e.g. `NVDA`"
                "for Nvidia, `AAPL` for Apple), and click **Run analysis**. You'll get a live price, a "
                "sentiment score and a recommendation card within a few seconds.",
            ),
            (
                "I don't know the ticker symbol for a company — what do I type?",
                "Type the company name (e.g. `nvidia`, `apple`, `tesla`) — NewsTicker recognizes many common "
                "company names and converts them to the right ticker automatically. If it's not recognized, "
                "search \"[company name] stock ticker\" online to find the exact symbol.",
            ),
        ],
    },
    {
        "category": "Free vs. Premium",
        "items": [
            (
                "What's the difference between Free and Premium?",
                "Free gives you 3 analyses per day, limited to U.S. markets only. Premium ($19.99, unlocks "
                "30 days of access) removes the daily limit entirely and unlocks international markets (add "
                "a suffix like `.DE`, `.UK`, `.RO` to the ticker), plus additional signal sources.",
            ),
            (
                "Does Premium auto-renew?",
                "No. Premium is a one-time purchase that grants 30 days of access. It does not auto-renew or "
                "charge you again automatically — after 30 days your account simply reverts to the Free plan"
                " and you can purchase Premium again any time.",
            ),
            (
                "How do I know how many days of Premium I have left?",
                "Currently the account badge shows your plan as Premium while it's active; if you're close "
                "to expiry, feel free to check your most recent payment confirmation email for the exact "
                "date it unlocked.",
            ),
        ],
    },
    {
        "category": "How the Analysis Works",
        "items": [
            (
                "Is this financial advice?",
                "No. NewsTicker generates fully automated analysis from public news and price data — "
                "it is not personal advice from a licensed financial advisor and it doesn't know your "
                "personal financial situation. Always do your own research and consult a licensed "
                "professional before making investment decisions. See our [Terms of Service](?legal=terms) "
                "for the full disclaimer.",
            ),
            (
                "Where does the news data come from?",
                "Public financial news sources indexed via Google News, covering outlets like Yahoo Finance, "
                "CNBC, TheStreet, Finviz and others. Premium also includes Reddit news for U.S. tickers.",
            ),
            (
                "What does the 'Confidence threshold' slider do?",
                "It sets how strongly the news sentiment needs to lean bullish or bearish before NewsTicker "
                "issues a firm BUY/SELL signal instead of a neutral \"stay on the sidelines\" read. "
                "Raising it makes the system more cautious; lowering it makes it react to weaker signals.",
            ),
            (
                "Why does it sometimes say 'insufficient data' or show a warning about a low sample?",
                "Some tickers, especially smaller or less-covered companies, simply don't have many recent "
                "news articles. When there are very few directional headlines, the sentiment percentage is "
                "statistically less reliable, so NewsTicker flags this explicitly instead of pretending to "
                "be more confident than the data supports.",
            ),
        ],
    },
    {
        "category": "Payments & Billing",
        "items": [
            (
                "What payment methods do you accept?",
                "Payments are processed securely through PayPal — you can pay with a PayPal balance, linked "
                "bank account, or debit/credit card, without needing a PayPal account for card payments.",
            ),
            (
                "Can I get a refund?",
                "Because Premium access is granted immediately upon payment, we generally don't offer "
                "refunds for change of mind. We do refund billing errors (double charges or payment received "
                "without access granted). See our full [Refund Policy](?legal=refund) for details.",
            ),
            (
                "Is my payment information safe?",
                "Yes — NewsTicker never sees or stores your card number or PayPal password. Payment happens "
                "entirely on PayPal's own secure page; we only receive a confirmation that the payment succeeded.",
            ),
        ],
    },
    {
        "category": "Privacy & Account",
        "items": [
            (
                "What data do you store about me?",
                "Your email, username, a securely hashed password, your watchlist, a short history of your "
                "past analyses, and your subscription status. Full details in our "
                "[Privacy Policy](?legal=privacy).",
            ),
            (
                "How do I delete my account?",
                "Contact us using the email listed in the Privacy Policy, and we'll delete your account and "
                "personal data within 30 days.",
            ),
            (
                "Can I use NewsTicker on multiple devices?",
                "Yes — just log in with the same account from any device or browser. Your watchlist and "
                "analysis history follow your account, not your device.",
            ),
        ],
    },
]
def render_faq_page():
    st.title("Frequently Asked Questions")
    st.write("")
    for section in FAQ_SECTIONS:
        st.subheader(section["category"])
        for question, answer in section["items"]:
            with st.expander(question):
                st.markdown(answer)
        st.write("")
    st.write("---")
    st.markdown(
        "Didn't find what you were looking for? Reach out via the contact email listed in our "
        "[Privacy Policy](?legal=privacy)."
    )