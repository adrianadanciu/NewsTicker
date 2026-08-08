import streamlit as st
import requests #library used to get in contact with the sites
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com" #the address which sends all the requests to paypal
PREMIUM_PRICE_USD = "19.99"
PREMIUM_DAYS = 30
def _get_paypal_access_token():
    client_id = st.secrets["PAYPAL_CLIENT_ID"]
    client_secret = st.secrets["PAYPAL_CLIENT_SECRET"]
    response = requests.post( #sends a POST request (request in which something is taken from the base and used to receive anoter information)
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]
def create_paypal_order():
    base_url = st.secrets.get("APP_BASE_URL", "http://localhost:8501") #gets the base address of the app after the payment
    access_token = _get_paypal_access_token() #gets access
    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders", #v2 is the version of paypal
        headers={"Authorization": f"Bearer {access_token}"}, #Bearer is the type of the token
        json={
            "intent": "CAPTURE", #CAPTURE means the money are transferred instantly
            "purchase_units": [{ #purchase description list
                "amount": {"currency_code": "USD", "value": PREMIUM_PRICE_USD},
                "description": "NewsTicker Premium - 30 days",
            }],
            "application_context": {
                "return_url": base_url,
                "cancel_url": base_url,
                "user_action": "PAY_NOW",
            },
        },
        timeout=10,
    )
    response.raise_for_status()
    order = response.json()
    approve_link = next(link["href"] for link in order["links"] if link["rel"] == "approve")
    return approve_link
def capture_paypal_order(order_id):
    """This function decides if the user is upgraded to Premium or not."""
    try:
        access_token = _get_paypal_access_token()
        response = requests.post(
            f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={},
            timeout=10,
        )
        if response.status_code not in (200, 201):
            st.session_state.paypal_debug = f"HTTP {response.status_code}: {response.text}"
            return False
        order = response.json()
        if order.get("status") != "COMPLETED":
            st.session_state.paypal_debug = f"order status = {order.get('status')} | full response: {order}"
            return False
        capture = order["purchase_units"][0]["payments"]["captures"][0]
        if capture.get("status") != "COMPLETED":
            st.session_state.paypal_debug = f"capture status = {capture.get('status')}"
            return False
        if capture["amount"]["value"] != PREMIUM_PRICE_USD:
            st.session_state.paypal_debug = f"incorrect amount: {capture['amount']['value']} (expected {PREMIUM_PRICE_USD})"
            return False
        return True
    except Exception as e:
        st.session_state.paypal_debug = f"Exception: {repr(e)}"
        return False
def render_paypal_button():
    try:
        approve_link = create_paypal_order()
    except Exception as e:
        st.error(f"We couldn't start the payment: {e}")
        return
    st.link_button("💳 Pay with PayPal — $19.99", approve_link, use_container_width=True)