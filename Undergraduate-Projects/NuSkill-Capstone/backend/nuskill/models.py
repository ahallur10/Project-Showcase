import os
import sqlite3
from contextlib import contextmanager
from .config import USE_SQLITE

# Optional: Snowflake support (not required in mock mode)
try:
    import snowflake.connector
except Exception:
    snowflake = None

def _sqlite_path():
    return os.path.join(os.path.dirname(__file__), "..", "..", "sql", "demo.db")

@contextmanager
def get_db():
    if USE_SQLITE:
        conn = sqlite3.connect(_sqlite_path())
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    else:
        if not snowflake:
            raise RuntimeError("Snowflake connector not available")
        conn = snowflake.connector.connect(
            user=os.getenv("SNOW_USER"),
            password=os.getenv("SNOW_PASS"),
            account=os.getenv("SNOW_ACCOUNT"),
            warehouse=os.getenv("SNOW_WH"),
            database=os.getenv("SNOW_DB"),
            schema=os.getenv("SNOW_SCHEMA", "PUBLIC"),
        )
        try:
            yield conn
        finally:
            conn.close()

def fetch_one(q, params=()):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(q, params)
        return cur.fetchone()

def fetch_all(q, params=()):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(q, params)
        return cur.fetchall()

def execute(q, params=()):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(q, params)
        conn.commit()

def init_demo_db():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "sql", "schema.sql")
    seed_path = os.path.join(os.path.dirname(__file__), "..", "..", "sql", "seed.sql")
    with get_db() as conn:
        cur = conn.cursor()
        with open(schema_path, "r") as f:
            cur.executescript(f.read())
        with open(seed_path, "r") as f:
            cur.executescript(f.read())
        conn.commit()
    print("Demo DB initialized at", _sqlite_path())
