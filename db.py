import streamlit as st
import psycopg2 #connects to supabase
import psycopg2.extras #library used to obtain results as dictionaries
from psycopg2 import pool
from contextlib import contextmanager
from datetime import datetime
@st.cache_resource(show_spinner=False)
def _get_pool():
    return pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=st.secrets["DB_URL"],
        connect_timeout=10,
    )
@contextmanager
def get_connection():
    conn_pool = _get_pool()
    conn = conn_pool.getconn()
    conn.autocommit = True
    try:
        yield conn
    finally:
        conn_pool.putconn(conn)
def init_db():
    """Creates the users table."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    plan TEXT NOT NULL DEFAULT 'Free',
                    upgrade_requested BOOLEAN NOT NULL DEFAULT FALSE,
                    usage_last_date TEXT NOT NULL DEFAULT '',
                    usage_count INTEGER NOT NULL DEFAULT 0,
                    last_ticker TEXT NOT NULL DEFAULT '',
                    watchlist JSONB NOT NULL DEFAULT '[]'::jsonb,
                    analysis_history JSONB NOT NULL DEFAULT '[]'::jsonb,
                    last_analysis JSONB
                );
                """
            )
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS premium_until TEXT NOT NULL DEFAULT '';")
def fetch_all_users_full():
    """Returns all users."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur: #each line behaves as a dictionary
            cur.execute(
                """
                SELECT username, email, name, password, plan, upgrade_requested, usage_last_date, usage_count, last_ticker, watchlist, analysis_history, last_analysis, premium_until
                FROM users;
                """
            )
            rows = cur.fetchall()
    usernames = {}
    for row in rows:
        usernames[row["username"]] = {
            "email": row["email"],
            "name": row["name"],
            "password": row["password"],
            "plan": row["plan"],
            "upgrade_requested": row["upgrade_requested"],
            "usage": {"last_date": row["usage_last_date"], "count": row["usage_count"]},
            "last_ticker": row["last_ticker"] or "",
            "watchlist": row["watchlist"] if row["watchlist"] is not None else [],
            "analysis_history": row["analysis_history"] if row["analysis_history"] is not None else [],
            "last_analysis": row["last_analysis"],
            "premium_until": row["premium_until"] or "",
        }
    return {"credentials": {"usernames": usernames}}
def create_user(username, email, name, hashed_password):
    """Registers a new user. Everyone starts on the Free plan -- no special-cased admin role."""
    plan = "Free"
    today_str = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (
                    username, email, name, password, plan, upgrade_requested,
                    usage_last_date, usage_count, last_ticker, watchlist, analysis_history, last_analysis
                )
                VALUES (%s, %s, %s, %s, %s, FALSE, %s, 0, '', '[]'::jsonb, '[]'::jsonb, NULL)
                ON CONFLICT (username) DO NOTHING;
                """,
                (username, email, name, hashed_password, plan, today_str),
            )
def upsert_user_full(username, user_data):
    """Saves all the fields of a user."""
    usage = user_data.get("usage") or {"last_date": "", "count": 0}
    last_analysis = user_data.get("last_analysis")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (
                    username, email, name, password, plan, upgrade_requested,
                    usage_last_date, usage_count, last_ticker, watchlist,
                    analysis_history, last_analysis, premium_until
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    password = EXCLUDED.password,
                    plan = EXCLUDED.plan,
                    upgrade_requested = EXCLUDED.upgrade_requested,
                    usage_last_date = EXCLUDED.usage_last_date,
                    usage_count = EXCLUDED.usage_count,
                    last_ticker = EXCLUDED.last_ticker,
                    watchlist = EXCLUDED.watchlist,
                    analysis_history = EXCLUDED.analysis_history,
                    last_analysis = EXCLUDED.last_analysis,
                    premium_until = EXCLUDED.premium_until;
                """,
                (
                    username,
                    user_data.get("email", ""),
                    user_data.get("name", username),
                    user_data["password"],
                    user_data.get("plan", "Free"),
                    user_data.get("upgrade_requested", False),
                    usage.get("last_date", ""),
                    usage.get("count", 0),
                    user_data.get("last_ticker", ""),
                    psycopg2.extras.Json(user_data.get("watchlist", [])),
                    psycopg2.extras.Json(user_data.get("analysis_history", [])),
                    psycopg2.extras.Json(last_analysis) if last_analysis is not None else None,
                    user_data.get("premium_until", ""),
                ),
            )
def save_all_users(config):
    for username, user_data in config["credentials"]["usernames"].items():
        upsert_user_full(username, user_data)