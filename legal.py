import streamlit as st
OPERATOR_NAME_PLACEHOLDER = "Adriana Danciu"
CONTACT_EMAIL_PLACEHOLDER = "ad.danciu@gmail.com"
LAST_UPDATED = "August 2026"
def render_terms_page():
    st.title("Terms of Service")
    st.caption(f"Last updated: {LAST_UPDATED}")
    st.markdown(f"""
By creating an account or using NewsTicker, you agree to these terms of service. NewsTicker is operated by 
**{OPERATOR_NAME_PLACEHOLDER}**. If you do not agree, please do not use the service.
### 1. What NewsTicker is
NewsTicker collects public financial news headlines from multiple sources, runs automated sentiment analysis 
(AI-based) on them and combines this with basic technical price indicators to produce an informational 
summary and a suggested trading signal (e.g. "BUY NOW", "HOLD", "STAY NEUTRAL").
### 2. Not financial advice
**This service does not provide financial, investment, tax, or legal advice.** All output is generated 
automatically from public data using automated rules and machine learning models, without human review of 
each individual case. Nothing in this site should be construed as a personal recommendation to buy, sell or
hold any financial instrument. You are solely responsible for your own investment decisions and their 
consequences, including any financial loss. Always do your own research and, where appropriate, consult a 
licensed, independent financial advisor.
### 3. Accounts
You must provide accurate information when registering and are responsible for keeping your login 
credentials confidential. You are responsible for all activity under your account.
### 4. Plans and pricing
- **Free plan**: limited to 3 analyses per day, U.S. markets only.
- **Premium plan**: a one-time payment of $19.99 grants 30 days of unlimited access and full global market
coverage. Premium access does **NOT** auto-renew; it must be purchased again after expiry.
Prices may change at any time for future purchases; changes do not affect access already granted.
### 5. Payments
Payments are processed by PayPal. We do not store your card or PayPal account credentials. See our 
[Privacy Policy](#) for details on what payment-related data we do retain (transaction status and date only).
### 6. Refunds
See our separate Refund Policy for full details on cancellations and refunds.
### 7. Acceptable use
You agree not to: attempt to get around usage limits through multiple accounts created to abuse the Free 
tier; scrape, resell, or redistribute the service's output at scale without permission; attempt to interfere 
with or disrupt the site's infrastructure.
### 8. Service availability
The Service is provided "as is" and "as available." Market data, news sources, and price feeds depend on 
third-party providers (e.g. Yahoo Finance, Google News) that we do not control and that may be delayed,
incomplete, or temporarily unavailable. We do not guarantee uninterrupted or error-free operation.
### 9. Limitation of liability
To the maximum extent permitted by law, the operator shall not be liable for any indirect, incidental or 
consequential damages, including trading losses, arising from your use of or reliance on the service. Our 
total liability for any claim arising from these terms or the service shall not exceed the amount you paid 
us in the 30 days preceding the claim.
### 10. Termination
We may suspend or terminate accounts that violate these terms. You may stop using the site and request 
deletion of your account at any time (see Privacy Policy for how).
### 11. Governing law
These Terms are governed by the laws of Romania, without regard to conflict of law principles. Any dispute 
shall be subject to the jurisdiction of the Romanian courts, without prejudice to any mandatory 
consumer-protection rights you may have under EU law as a consumer residing in another EU member state.
### 12. Contact
Questions about these Terms: **{CONTACT_EMAIL_PLACEHOLDER}**
""")
def render_privacy_page():
    st.title("Privacy Policy")
    st.caption(f"Last updated: {LAST_UPDATED}")
    st.markdown(f"""
This Privacy Policy explains what personal data NewsTicker, operated by **{OPERATOR_NAME_PLACEHOLDER}**, collects, why
and what rights you have over it, in line with the EU General Data Protection Regulation (GDPR).
### 1. What we collect
- **Account data**: email address, username, a securely hashed password (we never store your plain-text 
password).
- **Usage data**: your subscription plan, daily analysis count, your watchlist of tickers and a short 
history of your past analyses (ticker, signal, timestamp) — stored so the app can show you your own history.
- **Payment status**: whether you've purchased Premium and the expiry date. We do **not** receive or store 
your card number, PayPal password or any other payment credentials — those are handled entirely by PayPal.
- **Authentication cookie**: a browser cookie that keeps you logged in between visits.
### 2. Why we collect it (legal basis)
- To provide the Service you signed up for (contract performance) — account data, usage data.
- To process your Premium purchase (contract performance) — payment status.
- To keep you logged in (legitimate interest) — the auth cookie.
We do not use your data for advertising and we do not sell your data to third parties.
### 3. Where your data is stored
Your account data is stored in a Postgres database hosted by Supabase, in the EU (Frankfurt, Germany region). 
Payment processing happens on PayPal's own infrastructure; we only receive confirmation of success/failure.
### 4. Third parties who process your data
- **Supabase** (database hosting, EU-based)
- **PayPal** (payment processing)
- **Yahoo Finance / Google News** (we send them the ticker/company you search for, to fetch prices and news
— no personal account data is sent to them.
### 5. How long we keep your data
We keep your account and usage data for as long as your account is active. If you delete your account 
(see below), we delete your personal data within 30 days, except where we are legally required to retain 
payment records for tax/accounting purposes.
### 6. Your rights (GDPR)
You have the right to: access the personal data we hold about you; correct inaccurate data; request deletion 
of your account and data; export your data in a portable format; object to processing based on legitimate
interest. To exercise any of these rights, contact us at
**{CONTACT_EMAIL_PLACEHOLDER}**.
### 7. Cookies
We use one essential cookie for authentication (keeping you logged in). We do not use tracking or
advertising cookies.
### 8. Children
NewsTicker is not directed at children under 18 and we do not knowingly collect data from them.
### 9. Changes to this policy
We may update this policy from time to time. Material changes will be noted with an updated "Last updated" 
date above.
### 10. Contact
Questions about this policy or your data: **{CONTACT_EMAIL_PLACEHOLDER}**
""")
def render_refund_page():
    st.title("Refund Policy")
    st.caption(f"Last updated: {LAST_UPDATED}")
    st.markdown(f"""
This policy explains how refunds work for NewsTicker Premium purchases.
### 1. What you're buying
Premium is a **one-time purchase** ($19.99) that unlocks 30 days of full access. It is not a recurring 
subscription — it does not auto-renew and you will not be charged again unless you actively purchase 
Premium again.
### 2. Your EU right of withdrawal and immediate access
Under EU consumer protection law, purchases of digital content/services normally come with a 14-day 
"cooling-off" right of withdrawal. However, because Premium access is granted **immediately** upon 
successful payment, by completing your purchase you expressly request immediate performance and acknowledge 
that you lose your right of withdrawal once access has been granted, in accordance with applicable EU 
distance-selling rules.
### 3. Refund eligibility
Because access is granted instantly and usage cannot be "returned," we do not offer refunds for change of 
mind once Premium access has been unlocked.
We **will** issue a full refund if:
- You were charged but never received Premium access due to a technical error on our side (contact us with
your payment confirmation).
- You were charged twice for the same purchase due to a processing error.
### 4. How to request a refund
Contact **{CONTACT_EMAIL_PLACEHOLDER}** with your account email and PayPal transaction ID. We aim to respond 
within 5 business days.
### 5. Disputes and chargebacks
If you believe a charge was made in error, please contact us directly first — most issues can be resolved 
faster this way than through a PayPal dispute or bank chargeback.
""")