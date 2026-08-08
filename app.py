import streamlit as st
import base64
from datetime import datetime, timedelta
import theme
import auth
import sidebar
import results
import payments
import legal
import faq
#page configuration
st.set_page_config(page_title="NewsTicker", layout="wide")
theme.inject_custom_ui()
#app logo
svg_code = """
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
    <defs>
        <linearGradient id='grad' x1='0%' y1='0%' x2='100%' y2='100%'>
            <stop offset='0%' style='stop-color:#00f2fe;stop-opacity:1' />
            <stop offset='100%' style='stop-color:#4facfe;stop-opacity:1' />
        </linearGradient>
    </defs>
    <rect width='100' height='100' rx='25' fill='#0e1117'/>
    <path d='M20,50 L40,50 L55,25 L70,75 L85,50' fill='none' stroke='url(#grad)' stroke-width='8' stroke-linecap='round' stroke-linejoin='round'/>
    <circle cx='20' cy='50' r='5' fill='#00f2fe'/>
    <circle cx='85' cy='50' r='5' fill='#4facfe'/>
</svg>
"""
b64_svg = base64.b64encode(svg_code.encode('utf-8')).decode('utf-8')
custom_favicon = f"data:image/svg+xml;base64,{b64_svg}"
st.set_page_config(
    page_title="NewsTicker",
    page_icon=custom_favicon,
    layout="wide"
)
theme.inject_custom_ui()
#initialise memory
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "all_headlines" not in st.session_state:
    st.session_state.all_headlines = []
if "current_price" not in st.session_state:
    st.session_state.current_price = None
if "ai_stats" not in st.session_state:
    st.session_state.ai_stats = None
if "active_ticker" not in st.session_state:
    st.session_state.active_ticker = ""
if "checkout_mode" not in st.session_state:
    st.session_state.checkout_mode = False
if "watchlist_mode" not in st.session_state:
    st.session_state.watchlist_mode = False
if "legal_page" not in st.session_state:
    st.session_state.legal_page = None
if "faq_page" not in st.session_state:
    st.session_state.faq_page = False
#legal pages
if st.query_params.get("legal") in ("terms", "privacy", "refund"):
    st.session_state.legal_page = st.query_params.get("legal")
    st.query_params.clear()
    st.rerun()
if st.session_state.legal_page:
    if st.button("← Back"):
        st.session_state.legal_page = None
        st.rerun()
    if st.session_state.legal_page == "terms":
        legal.render_terms_page()
    elif st.session_state.legal_page == "privacy":
        legal.render_privacy_page()
    elif st.session_state.legal_page == "refund":
        legal.render_refund_page()
    st.stop()
#faq page
if st.query_params.get("faq") == "1":
    st.session_state.faq_page = True
    st.query_params.clear()
    st.rerun()
if st.session_state.faq_page:
    if st.button("← Back"):
        st.session_state.faq_page = False
        st.rerun()
    faq.render_faq_page()
    st.stop()
config = auth.load_config()
authenticator = auth.get_authenticator(config)
auth_status = st.session_state.get("authentication_status")
if auth_status is True:
    theme.inject_custom_ui()
    current_username = st.session_state["username"]
    user_data = config['credentials']['usernames'][current_username]
    user_plan = user_data.get('plan', 'Free')
    upgrade_requested = user_data.get('upgrade_requested', False)
    user_usage = auth.reset_daily_usage_if_needed(config, current_username)
    auth.check_premium_expiry(config, current_username)
    user_plan = config['credentials']['usernames'][current_username].get('plan', 'Free')
    results.restore_last_analysis(user_data)
    user_name = st.session_state.get('name', 'User')
    if st.query_params.get("trigger_upgrade") == "1":
        st.query_params.clear()
        st.session_state.checkout_mode = True
        st.rerun()
    paypal_token = st.query_params.get("token")
    if paypal_token:
        st.query_params.clear()
        if payments.capture_paypal_order(paypal_token):
            premium_until = (datetime.now() + timedelta(days=payments.PREMIUM_DAYS)).strftime("%Y-%m-%d")
            config['credentials']['usernames'][current_username]['plan'] = 'Premium'
            config['credentials']['usernames'][current_username]['upgrade_requested'] = False
            config['credentials']['usernames'][current_username]['premium_until'] = premium_until
            auth.save_config(config)
            st.session_state.checkout_mode = False
            st.session_state.paypal_success = True
        else:
            st.session_state.paypal_error = True
        st.rerun()
    if st.query_params.get("trigger_logout") == "1":
        st.query_params.clear()
        authenticator.logout(location='unrendered')
        st.rerun()
    if st.session_state.pop("paypal_success", False):
        st.success("✓ Payment confirmed — your account has been upgraded to Premium for 30 days!")
    if st.session_state.pop("paypal_error", False):
        st.error("✕ We couldn't confirm this payment with PayPal. If you were charged, please contact support.")
    if st.session_state.checkout_mode or st.session_state.watchlist_mode:
        if st.sidebar.button("← Back to Analysis", use_container_width=True):
            st.session_state.checkout_mode = False
            st.session_state.watchlist_mode = False
            st.rerun()
        st.sidebar.write("---")
    if st.session_state.checkout_mode and user_plan == "Free":
        sidebar.render_upgrade_page(config, current_username, auth.save_config)
    elif st.session_state.watchlist_mode:
        results.render_watchlist_page(config, current_username, auth.save_config, user_plan, user_usage)
    else:
        title_html = """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 46px; height: 46px; min-width: 46px;">
                <defs><linearGradient id="main_grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00f2fe;stop-opacity:1" /><stop offset="100%" style="stop-color:#4facfe;stop-opacity:1" /></linearGradient></defs>
                <rect width="100" height="100" rx="25" fill="#0e1117"/><path d="M20,50 L40,50 L55,25 L70,75 L85,50" fill="none" stroke="url(#main_grad)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="20" cy="50" r="6" fill="#00f2fe"/><circle cx="85" cy="50" r="6" fill="#4facfe"/>
            </svg>
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; color: #ffffff; font-family: 'Segoe UI', -apple-system, sans-serif;">NewsTicker</h1>
        </div>
        """
        st.markdown(title_html, unsafe_allow_html=True)
        if user_plan == "Free":
            limit_left = max(0, 3 - user_usage['count'])
            st.warning(f"ℹ️ You are on the **Free** plan. You have **{limit_left} out of 3 daily analyses** left.")
        st.write("---")
        option, target_company, confidence_threshold, run_analysis = sidebar.render_configuration_panel(
            user_data, config, current_username, auth.save_config, user_plan, upgrade_requested, user_name
        )
        if run_analysis:
            if user_plan == "Free":
                if "." in target_company:
                    st.error("✕ Access Denied: International markets require Premium plan.")
                    st.stop()
                if user_usage['count'] >= 3:
                    st.error("✕ Daily limit reached.")
                    st.stop()
            if not target_company:
                st.warning("Please enter a valid ticker first.")
            else:
                results.run_analysis_pipeline(
                    target_company, option, user_plan, user_usage, config, current_username, auth.save_config
                )
        if not st.session_state.analysis_done:
            results.render_intro_card(target_company, option, user_plan)
        else:
            results.render_dashboard(target_company, option, user_plan, confidence_threshold)
else:
    if auth_status is False:
        st.error('Username or password incorrect.')
    auth.render_login_page(authenticator, config)

st.write("")
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0; margin-top: 20px;">
        <a href="?faq=1" target="_self" style="color: #64748b; font-size: 0.8rem; text-decoration: none; margin: 0 10px;">FAQ</a>
        <a href="?legal=terms" target="_self" style="color: #64748b; font-size: 0.8rem; text-decoration: none; margin: 0 10px;">Terms of Service</a>
        <a href="?legal=privacy" target="_self" style="color: #64748b; font-size: 0.8rem; text-decoration: none; margin: 0 10px;">Privacy Policy</a>
        <a href="?legal=refund" target="_self" style="color: #64748b; font-size: 0.8rem; text-decoration: none; margin: 0 10px;">Refund Policy</a>
    </div>
    """,
    unsafe_allow_html=True,
)