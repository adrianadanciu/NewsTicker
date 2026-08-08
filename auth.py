import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import db as db_manager
def load_config():
    """Loads all the users from Suprabase."""
    db_manager.init_db()
    config = db_manager.fetch_all_users_full()
    config['cookie'] = {
        'name': st.secrets.get('COOKIE_NAME', 'auth_cookie'),
        'key': st.secrets.get('COOKIE_KEY', 'signature_key'),
        'expiry_days': 30,
    }
    return config
def save_config(config):
    db_manager.save_all_users(config)
def get_authenticator(config):
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
def reset_daily_usage_if_needed(config, username):
    """Resets the daily analysis counter if it's a new day."""
    user_data = config['credentials']['usernames'][username]
    today_str = datetime.now().strftime("%Y-%m-%d")
    user_usage = user_data.get('usage', {'last_date': today_str, 'count': 0})
    if user_usage['last_date'] != today_str:
        user_usage['last_date'] = today_str
        user_usage['count'] = 0
        config['credentials']['usernames'][username]['usage'] = user_usage
        save_config(config)
    return user_usage
def check_premium_expiry(config, username):
    user_data = config['credentials']['usernames'][username]
    if user_data.get('plan') != 'Premium':
        return
    premium_until = user_data.get('premium_until', '')
    if not premium_until:
        return
    today_str = datetime.now().strftime("%Y-%m-%d")
    if today_str > premium_until:
        config['credentials']['usernames'][username]['plan'] = 'Free'
        config['credentials']['usernames'][username]['premium_until'] = ''
        save_config(config)
def render_login_page(authenticator, config):
    """Renders the logged-out welcome screen with Login/Register tabs."""
    title_welcome_html = """
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 54px; height: 54px; min-width: 54px;">
            <defs>
                <linearGradient id="welcome_grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#00f2fe;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#4facfe;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="100" height="100" rx="25" fill="#0e1117"/>
            <path d="M20,50 L40,50 L55,25 L70,75 L85,50" fill="none" stroke="url(#welcome_grad)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="20" cy="50" r="6" fill="#00f2fe"/>
            <circle cx="85" cy="50" r="6" fill="#4facfe"/>
        </svg>
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800; color: #ffffff; font-family: 'Segoe UI', -apple-system, sans-serif;">NewsTicker</h1>
    </div>
    """
    st.markdown(title_welcome_html, unsafe_allow_html=True)
    intro_html = """
    <div style="background: rgba(19, 41, 75, 0.95); border-radius: 16px; box-shadow: 0 15px 40px rgba(0, 242, 254, 0.15); border-left: 4px solid #00f2fe; padding: 24px 30px; margin-bottom: 25px;">
        <h2 style="color: #ffffff; margin-top: 0; margin-bottom: 10px; font-weight: 800; font-size: 1.5rem;">Know what the market is thinking before you trade</h2>
        <p style="color: #cbd5e1; font-size: 0.98rem; line-height: 1.6; margin: 0 0 16px 0;">
            NewsTicker scans live financial headlines, scores their sentiment, and cross-checks it against real price trends —
            so you get a clear read on the market instead of scrolling through dozens of articles yourself.
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 20px; font-size: 0.9rem; color: #cbd5e1;">
            <div>▲ <b>Live news sentiment</b> across global markets</div>
            <div>▬ <b>Candlestick charts</b> from 1H to 1Y</div>
            <div>★ <b>Exact entry price targets</b> — not just "buy" or "sell", but at what price</div>
        </div>
    </div>
    """
    st.markdown(intro_html, unsafe_allow_html=True)
    st.write("### Create your free account to see it in action:")
    tab_login, tab_register = st.tabs(["Login", "Register"])
    with tab_login:
        authenticator.login()
    with tab_register:
        try:
            register_result = authenticator.register_user(password_hint=False)
            if register_result:
                email, username, name = register_result
                if username:
                    hashed_password = config['credentials']['usernames'][username]['password']
                    db_manager.create_user(username, email, name, hashed_password)
                    st.success('✓ Account created successfully! Switch to the "Login" tab to sign in.')
        except Exception as e:
            st.error(f"Registration error: {e}")

    st.markdown(
        """
        <p style="color: #64748b; font-size: 0.75rem; line-height: 1.4; margin-top: 20px; text-align: center;">
            By creating an account, you acknowledge that NewsTicker provides automated,
            AI-generated market analysis for informational purposes only — it is not
            financial, investment, or tax advice from a licensed professional. Trading
            involves risk of loss. You are solely responsible for your own investment decisions.
        </p>
        """,
        unsafe_allow_html=True,
    )