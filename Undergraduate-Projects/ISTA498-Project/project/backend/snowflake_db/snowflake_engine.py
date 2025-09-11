# snowflake_db/snowflake_engine.py

from datetime import datetime
from time import time
from dotenv import load_dotenv
load_dotenv()

import os
import sys
sys.path.insert(0, '../')
from tutorial.tutorial import Tutorial  # keeping original import
import schedule  # may be unused, but keeping to avoid side-effects in other files

# =====================================================================================
# Config / Mock Toggle
# =====================================================================================
USE_MOCK = os.getenv("USE_MOCK", "1") == "1"  # default ON so dev works without Snowflake

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")  # fixed typo
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "ISTA498WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "NUSKILL")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "NUSKILL_MASTER")

def _connect_snowflake():
    """Return a Snowflake connection or None (in mock mode or on failure)."""
    if USE_MOCK:
        print("[snowflake_engine] USE_MOCK=1 → skipping Snowflake connection.")
        return None
    try:
        import snowflake.connector  # import only when needed
        print("[snowflake_engine] Connecting to Snowflake…")
        ctx = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
        )
        # Select default DB/Warehouse if provided
        cs = ctx.cursor()
        try:
            cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
            cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        finally:
            cs.close()
        return ctx
    except Exception as e:
        print(f"[snowflake_engine] Snowflake connect failed: {e}")
        return None

ctx = _connect_snowflake()

# =====================================================================================
# Simple in-memory MOCK DATA so the UI can render without a DB
# =====================================================================================
_mock_users = {
    # user_id: (hashed_password, total_deposited, current_balance)
    "user_test_5": ("test_pw", 200.0, 200.0),
    "demo_user": ("demo_pw", 50.0, 35.0),
}

_mock_deposits = [
    # (user_id, amt, amt_earned_back, total_checks_allwd)
    ("user_test_5", 5.0, 0.0, 5),
    ("user_test_5", 10.0, 0.0, 11),
    ("demo_user", 20.0, 0.0, 24),
]

_mock_genre_videos = {
    # genre: [urls...]
    "Snapchat": [
        "https://youtu.be/FD4hqhlc3Aw",
        "https://youtu.be/9-NDblKPNfg",
        "https://youtu.be/xFdu-WDfEPk",
    ],
    "Dog Training": [
        "https://youtu.be/f_X-0VJJUL8",
        "https://youtu.be/ng58pNPDDW4",
        "https://youtu.be/EBoJym_wQ2M",
    ],
}

_mock_video_objects = {
    # url: (name, url, checks, series(bool), genre)
    "https://youtu.be/FD4hqhlc3Aw": ("Snapchat 1", "https://youtu.be/FD4hqhlc3Aw", 5, True, "Snapchat"),
    "https://youtu.be/9-NDblKPNfg": ("Snapchat 2", "https://youtu.be/9-NDblKPNfg", 5, True, "Snapchat"),
    "https://youtu.be/xFdu-WDfEPk": ("Snapchat 3", "https://youtu.be/xFdu-WDfEPk", 5, True, "Snapchat"),
    "https://youtu.be/f_X-0VJJUL8": ("Dog Training 1", "https://youtu.be/f_X-0VJJUL8", 5, True, "Dog Training"),
    "https://youtu.be/ng58pNPDDW4": ("Dog Training 2", "https://youtu.be/ng58pNPDDW4", 5, True, "Dog Training"),
    "https://youtu.be/EBoJym_wQ2M": ("Dog Training 3", "https://youtu.be/EBoJym_wQ2M", 5, True, "Dog Training"),
}

# =====================================================================================
# Helpers
# =====================================================================================
def _checks_allowed_for_amount(amt: float) -> int:
    if 0.00 < amt <= 5.00:
        return 5
    if amt <= 10.00:
        return 11
    if amt <= 20.00:
        return 24
    if amt <= 50.00:
        return 52
    if amt <= 100.00:
        return 112
    return 0

# =====================================================================================
# Public Functions (kept same names/signatures).
# Each supports both real Snowflake and mock behavior.
# =====================================================================================

def insert_user(id, password):
    if ctx is None:
        # Mock: insert/update memory
        total = 0.0
        curr = 0.0 if "test" in id else 0.0  # original code gave test users 200; keep that if you like
        if "test" in id:
            curr = 200.0
        _mock_users[id] = (password, total, curr)
        return
    # REAL
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        # NOTE: this string concatenation is vulnerable to SQL injection; use binds in production.
        if 'test' not in id:
            cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."USER_DATA"(USER_ID,HASHED_PASSWORD,TOTAL_DEPOSITED,CURRENT_BALANCE)
                           VALUES('{id}','{password}','0','0');''')
        else:
            cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."USER_DATA"(USER_ID,HASHED_PASSWORD,TOTAL_DEPOSITED,CURRENT_BALANCE)
                           VALUES('{id}','{password}','0','200');''')
    finally:
        cs.close()

def get_user(id):
    if ctx is None:
        # Mock returns list of tuples like original Snowflake fetchall
        rec = _mock_users.get(id)
        if not rec:
            return []
        hashed_password, total_deposited, current_balance = rec
        return [(id, hashed_password, total_deposited, current_balance)]
    # REAL
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''SELECT * FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."USER_DATA" WHERE USER_ID ='{id}';''')
        cs.get_results_from_sfqid(cs.sfqid)
        try:
            results = cs.fetchall()
        except:
            results = []
        return results
    finally:
        cs.close()

def get_user_password(id):
    res = get_user(id)
    if not res:
        return None
    # original assumed tuple order: (user_id, password, total_deposited, current_balance)
    password = res[0][1]
    return password

def get_user_balance(id):
    res = get_user(id)
    if not res:
        return None
    _, _, _, current_balance = res[0]
    return current_balance

def insert_user_deposited(id, amt):
    amt = float(amt)
    checks = _checks_allowed_for_amount(amt)
    if ctx is None:
        _mock_deposits.append((id, amt, 0.0, checks))
        # also update user's totals
        if id in _mock_users:
            pw, total, curr = _mock_users[id]
            _mock_users[id] = (pw, total + amt, curr + amt)
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."DAILY_DEPOSITED"(USER_ID,AMT,AMT_EARNED_BACK,TOTAL_CHECKS_ALLWD)
                       VALUES('{id}','{amt}','0','{checks}');''')
    finally:
        cs.close()

def get_user_deposited(id=None):
    if ctx is None:
        if id:
            return [row for row in _mock_deposits if row[0] == id]
        return list(_mock_deposits)
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        if id:
            cs.execute(f'''SELECT * FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."DAILY_DEPOSITED" WHERE USER_ID ='{id}';''')
        else:
            cs.execute(f'''SELECT * FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."DAILY_DEPOSITED";''')
        cs.get_results_from_sfqid(cs.sfqid)
        results = cs.fetchall()
        return results
    finally:
        cs.close()

def insert_video_to_genre(genre, vid):
    if ctx is None:
        _mock_genre_videos.setdefault(genre, [])
        if vid not in _mock_genre_videos[genre]:
            _mock_genre_videos[genre].append(vid)
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        videos = get_genre_videos(genre)
        videos.append(vid)
        videos = str(videos).replace('[','').replace(']','')
        cs.execute(f'''UPDATE "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."GENRE_VIDEOS"
                       SET VID_LIST = ARRAY_CONSTRUCT({videos}) WHERE GENRE = '{genre}';''')
    finally:
        cs.close()

def insert_genre(genre, list_string=''):
    if ctx is None:
        _mock_genre_videos.setdefault(genre, [])
        return 'OK'
    genre_map = get_genre_map()
    if genre in genre_map.keys():
        return 'Genre exists'
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."GENRE_VIDEOS"(GENRE,VID_LIST)
                       SELECT $1, ARRAY_CONSTRUCT({list_string}) FROM VALUES ('{genre}');''')
    finally:
        cs.close()

def get_genre_map():
    if ctx is None:
        # return genre -> videos list
        return {g: list(vs) for g, vs in _mock_genre_videos.items()}
    genre_map = {}
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''SELECT GENRE FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."GENRE_VIDEOS";''')
        cs.get_results_from_sfqid(cs.sfqid)
        results = cs.fetchall()
        for (curr_genre,) in results:
            genre_map[curr_genre] = get_genre_videos(curr_genre)
        return genre_map
    finally:
        cs.close()

def get_genre_videos(genre):
    if ctx is None:
        return list(_mock_genre_videos.get(genre, []))
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''SELECT VID_LIST FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."GENRE_VIDEOS" WHERE GENRE = '{genre}';''')
        cs.get_results_from_sfqid(cs.sfqid)
        try:
            results = cs.fetchall()
            data = results[0]
            urls = data[0].replace('\n','').replace(' ','').replace('"','')
            urls = urls[1:-1].split(',')
            return urls
        except:
            return []
    finally:
        cs.close()

def insert_new_video(name, url, checks, series, genre):
    insert_genre(genre)
    insert_video_to_genre(genre=genre, vid=url)
    if ctx is None:
        _mock_video_objects[url] = (name, url, int(checks), bool(series), genre)
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."VIDEO_OBJECTS"(NAME,URL,CHECKS,SERIES,GENRE)
                       VALUES('{name}','{url}','{int(checks)}','{str(bool(series))}','{genre}');''')
    finally:
        cs.close()

def get_video_object(url):
    if ctx is None:
        if url not in _mock_video_objects:
            return None
        name, url, checks, series, genre = _mock_video_objects[url]
        return Tutorial(name, url, int(checks), series, genre)
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''SELECT * FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."VIDEO_OBJECTS" WHERE URL = '{url}';''')
        cs.get_results_from_sfqid(cs.sfqid)
        results = cs.fetchall()
        name, url, checks, series, genre = results[0]
        return Tutorial(name, url, int(checks), series, genre)
    finally:
        cs.close()

def add_user_video_status(user_obj, url, genre):
    if ctx is None:
        # no-op in mock; could record status in memory if the UI needs it
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        # NOTE: The original SQL had a syntax issue around column list (missing comma).
        cs.execute(f'''INSERT INTO "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."USER_VIDEO_STATUS"
                       (ID, URL, GENRE, IN_PROGRESS, COMPLETED)
                       VALUES('{str(user_obj.getWalletId())}','{url}','{genre}','TRUE','FALSE');''')
    finally:
        cs.close()

def update_user_video_status_completed(user_obj, url):
    if ctx is None:
        # no-op in mock
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'''UPDATE "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."USER_VIDEO_STATUS"
                       SET IN_PROGRESS = 'FALSE', COMPLETED = 'TRUE'
                       WHERE ID = '{str(user_obj)}' AND URL = '{url}';''')
    finally:
        cs.close()

def delete_daily_deposited():
    if ctx is None:
        _mock_deposits.clear()
        return
    cs = ctx.cursor()
    try:
        cs.execute(f'USE DATABASE "{SNOWFLAKE_DATABASE}";')
        cs.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}";')
        cs.execute(f'DELETE FROM "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."DAILY_DEPOSITED"')
    finally:
        cs.close()
