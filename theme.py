#this file contains all the visual theme of the app
import streamlit as st

def inject_custom_ui():
    custom_css = """
    <style>
        /*hides default clutter*/
        #MainMenu, footer, .stDeployButton,
        [data-testid="stAppDeployButton"],
        [data-testid="stToolbarActions"] {
            display: none !important;
        }
        /*transparent instead of display:none, so the sidebar re-open button inside it still works*/
        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }
        /*background color*/
        .stApp, .stMain {
            background: linear-gradient(145deg, #0a1f3d 0%, #13294b 50%, #1e3a6e 100%) !important;
        }
        /*sidebar color*/
        div[data-testid="stSidebar"], .stSidebar {
            background: #0a1f3d !important;
        }
        /*user profile aspect*/
        .profile-container, 
        div[data-testid="stSidebar"] > div:first-child,
        .profile-card {
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 8px 0 !important;
        }
        /*blocks aspect*/
        div[data-testid="stMetric"] {
            background: rgba(19, 41, 75, 0.9) !important;
            border-radius: 14px !important;
            box-shadow: 0 10px 30px rgba(0, 242, 254, 0.12) !important;
            padding: 28px 20px !important;
            min-height: 140px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricValue"] {
            width: 100% !important;
            text-align: center !important;
            justify-content: center !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 2.1rem !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            margin-bottom: 6px !important;
        }
        /*big cards aspect*/
        .premium-card {
            background: rgba(19, 41, 75, 0.95) !important;
            border-radius: 16px !important;
            box-shadow: 0 15px 40px rgba(0, 242, 254, 0.18) !important;
            padding: 24px 30px !important;
        }
        /*button aspect*/
        div.stButton button {
            background: linear-gradient(135deg, #1e3a6e, #13294b) !important;
            border: 2px solid #00f2fe !important;
            border-radius: 12px !important;
        }
        div.stButton button:hover {
            background: linear-gradient(135deg, #00f2fe, #64c8ff) !important;
            color: #0a1f3d !important;
        }
        /*main page organizing*/
        .block-container {
            padding-top: 0.8rem !important;
            padding-bottom: 2rem !important;
        }
        div[data-testid="stMain"] hr {
            margin: 0.4rem 0 !important;
        }
        div[data-testid="stMain"] div[data-testid="stMarkdownContainer"] p {
            margin: 0 !important;
        }
        div[data-testid="stSidebarUserContent"] {
            padding-top: 0.3rem !important;
            overflow: visible !important;
        }
        div[data-testid="stSidebar"],
        div[data-testid="stSidebar"] > div,
        div[data-testid="stSidebar"] section,
        div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"],
        div[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stSidebar"] div[data-testid="element-container"],
        div[data-testid="stSidebar"] div[data-testid="stElementContainer"],
        div[data-testid="stSidebar"] div[data-testid="stHtml"],
        div[data-testid="stSidebar"] div[data-testid="stMarkdown"],
        div[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
            overflow: visible !important;
            height: auto !important;
            min-height: 0 !important;
        }
        /*compacts the sidebar*/
        div[data-testid="stSidebarHeader"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            min-height: 0 !important;
            height: auto !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.05rem !important;
        }
        div[data-testid="stSidebar"] div[data-testid="element-container"],
        div[data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stHtml"],
        div[data-testid="stSidebar"] div[data-testid="stMarkdown"],
        div[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.1 !important;
        }
        div[data-testid="stSidebar"] div.stButton {
            margin: 0 !important;
        }
        div[data-testid="stSidebar"] div.stButton button {
            padding-top: 0.35rem !important;
            padding-bottom: 0.35rem !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
            margin: 0 !important;
        }
        div[data-testid="stSidebar"] hr {
            margin: 0.1rem 0 !important;
        }
        div[data-testid="stSidebar"] .stRadio {
            margin-bottom: -0.6rem !important;
        }
        div[data-testid="stSidebar"] label p {
            font-size: 0.85rem !important;
            margin-bottom: 2px !important;
        }
        /*ticker input aspect*/
        .st-key-ticker_input div[data-baseweb="input"] {
            background: rgba(0, 242, 254, 0.10) !important;
            border: 2px solid #00f2fe !important;
            border-radius: 12px !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.35) !important;
        }
        .st-key-ticker_input input {
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            text-align: center !important;
            letter-spacing: 2px !important;
            color: #00f2fe !important;
            background: transparent !important;
            padding: 14px !important;
        }
        .st-key-ticker_input div[data-baseweb="input"]:focus-within {
            box-shadow: 0 0 26px rgba(0, 242, 254, 0.55) !important;
        }
        .st-key-ticker_input div[data-testid="InputInstructions"] {
            display: none !important;
        }
    </style>
    <script>
    /*autoselects all text in the ticker box on focus, so typing replaces it*/
    if (!window.__tickerFocusSelectBound) {
        window.__tickerFocusSelectBound = true;
        document.addEventListener('focus', function (e) {
            if (e.target && e.target.matches && e.target.matches('.st-key-ticker_input input')) {
                e.target.select();
            }
        }, true);
    }
    </script>
    """
    st.html(custom_css)