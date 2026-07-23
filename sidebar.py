import streamlit as st
#lets the user type a company name instead of the exact ticker
COMPANY_NAME_TO_TICKER = {
    "nvidia": "NVDA", "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL",
    "alphabet": "GOOGL", "amazon": "AMZN", "tesla": "TSLA", "meta": "META",
    "facebook": "META", "netflix": "NFLX", "amd": "AMD", "intel": "INTC",
    "ibm": "IBM", "oracle": "ORCL", "salesforce": "CRM", "adobe": "ADBE",
    "paypal": "PYPL", "uber": "UBER", "airbnb": "ABNB", "coinbase": "COIN",
    "disney": "DIS", "walmart": "WMT", "target": "TGT", "mcdonalds": "MCD",
    "starbucks": "SBUX", "nike": "NKE", "visa": "V", "mastercard": "MA",
    "jpmorgan": "JPM", "bank of america": "BAC", "goldman sachs": "GS",
    "berkshire hathaway": "BRK.B", "exxon": "XOM", "chevron": "CVX",
    "pfizer": "PFE", "johnson johnson": "JNJ", "coca cola": "KO",
    "pepsi": "PEP", "boeing": "BA", "ford": "F", "general motors": "GM",
    "qualcomm": "QCOM", "cisco": "CSCO", "sony": "SONY", "spotify": "SPOT",
    "shopify": "SHOP", "palantir": "PLTR", "snowflake": "SNOW", "zoom": "ZM",
    "sap": "SAP.DE", "volkswagen": "VOW3.DE", "siemens": "SIE.DE",
    "hidroelectrica": "H2O.RO", "romgaz": "SNG.RO", "petrom": "SNP.RO",
    "banca transilvania": "TLV.RO", "bank transilvania": "TLV.RO",
}
def resolve_ticker(user_input: str) -> str:
    """Maps a recognized company name to its ticker"""
    key = user_input.strip().lower()
    return COMPANY_NAME_TO_TICKER.get(key, user_input)
#display of the profile
def render_profile_card(user_plan, upgrade_requested, user_name):
    first_letter = user_name[0].upper() if user_name else "U"
    if user_plan == "Premium":
        glow_color = "#f39c12"
        bg_gradient = "linear-gradient(135deg, #f39c12 0%, #d35400 100%)"
        border_accent = "rgba(243, 156, 18, 0.4)"
        plan_badge_style = "background: rgba(243, 156, 18, 0.15); border: 1px solid rgba(243, 156, 18, 0.4); color: #f1c40f;"
    else:
        glow_color = "#3498db"
        bg_gradient = "linear-gradient(135deg, #3498db 0%, #2c3e50 100%)"
        border_accent = "rgba(52, 152, 219, 0.4)"
        plan_badge_style = "background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); color: #94a3b8;"
    if user_plan == "Free":
        if upgrade_requested:
            action_html = "<div style='padding: 8px; border-radius: 6px; background-color: rgba(243, 156, 18, 0.1); border: 1px dashed #f39c12; color: #f39c12; font-size: 0.75rem; text-align: center; font-weight: 600;'>Upgrade processing...</div>"
        else:
            action_html = """
            <a href="?trigger_upgrade=1" target="_self" style="text-decoration: none !important;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 6px; background: linear-gradient(135deg, #f39c12 0%, #d35400 100%); color: white !important; font-size: 0.75rem; font-weight: 700; padding: 8px 12px; border-radius: 6px; cursor: pointer; text-align: center; box-shadow: 0 4px 10px rgba(243, 156, 18, 0.3); border: 1px solid rgba(255, 255, 255, 0.1);">★ UPGRADE TO PREMIUM</div>
            </a>
            """
    else:
        action_html = "<div style='font-size: 0.75rem; color: #8a90a6; text-align: center;'>You have full access.</div>"

    profile_menu_html = f"""
    <div class="profile-container" style="display: flex; align-items: center; gap: 12px; padding-bottom: 10px;">
        <div style="position: relative; display: flex; align-items: center; justify-content: center; width: 46px; height: 46px; flex-shrink: 0;">
            <div style="position: absolute; width: 46px; height: 46px; border-radius: 50%; border: 1.5px solid {glow_color}; opacity: 0.25; filter: blur(1.5px);"></div>
            <div style="width: 40px; height: 40px; background: {bg_gradient}; color: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.3rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1.5px solid {border_accent}; text-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 2;">{first_letter}</div>
            <div style="position: absolute; bottom: 0px; right: 0px; width: 10px; height: 10px; background-color: {glow_color}; border-radius: 50%; border: 2px solid #0e1117; box-shadow: 0 0 8px {glow_color}; z-index: 3;"></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 3px; min-width: 0;">
            <span style="font-size: 0.9rem; color: #f1f5f9; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{user_name}</span>
            <span style="display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.75px; width: fit-content; {plan_badge_style}">{user_plan}</span>
        </div>
    </div>
    <div style="margin-bottom: 10px;">{action_html}</div>
    """
    st.sidebar.html(profile_menu_html)
#checkout page
def render_upgrade_page(config, current_username, save_config):
    st.title("Unlock Premium Plan")
    st.markdown("### Take your portfolio and market analysis to a professional level")
    st.write("---")
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        st.markdown("""
        ### Why choose premium?
        * **Full global access:** Analyze markets worldwide (.DE, .UK, .JP, .FR, .RO etc.).
        * **Unlimited AI analyses:** Run as many searches as you want, every day.
        * **Entry/exit optimization:** Receive exact optimal entry limits, stop-loss triggers and asset management rules.
        * **Extended premium data:** Access to additional market signals and community sentiment sources.
        
        ### Price: **$19.99 / month**
        """)
    with col_pay2:
        st.subheader("Payment Method")
        st.info("Payments are processed securely. We currently accept direct transfer or rapid links.")
        st.markdown("[↗ Step 1: Click here to pay via Stripe / Revolut](https://stripe.com)")
        st.write("---")
        st.write("### Step 2: Confirm Payment")
        st.text_input("Name / Transaction ID:")
        if st.button("✓ Submit proof of payment for activation"):
            config['credentials']['usernames'][current_username]['plan'] = 'Premium'
            config['credentials']['usernames'][current_username]['upgrade_requested'] = False
            save_config(config)
            st.session_state.checkout_mode = False
            st.success("✓ Payment confirmed — your account has been upgraded to Premium!")
            st.rerun()
#sidebar configuration
def render_configuration_panel(user_data):
    """Renders the sidebar's configuration panel."""
    #title
    header_html = """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px; margin-top: 0px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 26px; height: 26px; min-width: 26px; display: block;">
            <defs><linearGradient id="header_grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00f2fe;stop-opacity:1" /><stop offset="100%" style="stop-color:#4facfe;stop-opacity:1" /></linearGradient></defs>
            <rect width="100" height="100" rx="25" fill="#1c1f26"/><path d="M20,50 L40,50 L55,25 L70,75 L85,50" fill="none" stroke="url(#header_grad)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><circle cx="20" cy="50" r="6" fill="#00f2fe"/><circle cx="85" cy="50" r="6" fill="#4facfe"/>
        </svg>
        <span style="font-size: 1.05rem; font-weight: 700; color: #f1f5f9; font-family: 'Segoe UI', -apple-system, sans-serif; letter-spacing: -0.2px; white-space: nowrap; line-height: 1;">Configuration Panel</span>
    </div>
    """
    st.sidebar.markdown(header_html, unsafe_allow_html=True)
    option = st.sidebar.radio("Select operation mode:", ("BUY", "SELL"), key="operation_mode")
    #ticker box
    def _submit_ticker():
        st.session_state.trigger_run = True
    if "ticker_input" not in st.session_state:
        st.session_state.ticker_input = user_data.get("last_ticker", "")
    target_company_input = st.sidebar.text_input(
        "Enter company ticker (ex: NVDA, AAPL):",
        placeholder="NVDA",
        key="ticker_input",
        on_change=_submit_ticker,
    ).strip()
    target_company_input = resolve_ticker(target_company_input).upper()
    guide_html = """
    <div style="background-color: #12162e; border-left: 3px solid #3498db; padding: 8px 10px; border-radius: 4px; margin-top: -8px; margin-bottom: 4px;">
        <span style="font-size: 0.9rem; color: #7885b0; line-height: 1.3; display: block;">The USA market is the system default.</span>
    </div>
    <div style="background-color: rgba(243, 156, 18, 0.1); border-left: 3px solid #f39c12; padding: 8px 10px; border-radius: 4px; margin-bottom: 10px;">
        <span style="font-size: 0.9rem; color: #f1c078; line-height: 1.3; display: block;"><b>⚠ Important — other countries:</b> add the ticker suffix (ex: <code>SAP.DE</code>).</span>
    </div>
    """
    st.sidebar.markdown(guide_html, unsafe_allow_html=True)
    confidence_threshold = st.sidebar.slider(
        "Confidence threshold (%)", min_value=50, max_value=80, value=60, step=1,
        help="Minimum bullish/bearish sentiment share required before the system issues a firm BUY/SELL signal.",
    )
    target_company = target_company_input if target_company_input else "NVDA"
    #keeps the last change
    if target_company != st.session_state.active_ticker:
        st.session_state.analysis_done = False
    run_analysis = st.sidebar.button("▶ Run analysis", use_container_width=True)
    if st.session_state.get("trigger_run"):
        run_analysis = True
        st.session_state.trigger_run = False
    return option, target_company, confidence_threshold, run_analysis