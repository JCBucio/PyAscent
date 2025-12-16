import sqlite3
from .config import CACHE_DB


_conn = None


def get_conn():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(CACHE_DB, check_same_thread=False)
        _init_db(_conn)
    return _conn


def _init_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS segments (
        id INTEGER PRIMARY KEY,
        json TEXT,
        last_fetch INTEGER
    )
    """)
    conn.commit()