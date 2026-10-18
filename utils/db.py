"""SQLite helpers + password hashing. Everything is stored inside the project folder (data/tourist.db)."""
import hashlib, hmac, os, sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tourist.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, full_name TEXT, email TEXT,
  pw_hash TEXT NOT NULL, salt TEXT NOT NULL, role TEXT DEFAULT 'tourist', created TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS places(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, region TEXT, area TEXT, station TEXT, category TEXT,
  description TEXT, dos TEXT, donts TEXT, best_time TEXT, entry_fee TEXT, lat REAL, lon REAL,
  wiki_title TEXT, image TEXT, youtube TEXT);
CREATE TABLE IF NOT EXISTS hotels(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, region TEXT, area TEXT, stars INTEGER,
  price_per_night TEXT, lat REAL, lon REAL, phone TEXT, description TEXT);
CREATE TABLE IF NOT EXISTS cafes(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, region TEXT, area TEXT, speciality TEXT,
  price_for_two TEXT, lat REAL, lon REAL, description TEXT);
CREATE TABLE IF NOT EXISTS chat_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, question TEXT, answer TEXT, ts TEXT DEFAULT CURRENT_TIMESTAMP);
"""

COLUMNS = {
    "places": ["name","region","area","station","category","description","dos","donts","best_time",
               "entry_fee","lat","lon","wiki_title","image","youtube"],
    "hotels": ["name","region","area","stars","price_per_night","lat","lon","phone","description"],
    "cafes": ["name","region","area","speciality","price_for_two","lat","lon","description"],
    "users": ["username","full_name","email","pw_hash","salt","role"],
}


def conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def hash_pw(password, salt=None):
    salt = salt or os.urandom(16).hex()
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return h, salt


def init_db():
    from utils import seed
    c = conn()
    try:
        c.executescript(SCHEMA)
        if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            h, s = hash_pw(os.getenv("ADMIN_PASSWORD", "admin123"))
            c.execute("INSERT INTO users(username,full_name,email,pw_hash,salt,role) VALUES(?,?,?,?,?,?)",
                      ("admin", "Administrator", "admin@mumbaiguide.local", h, s, "admin"))
        for table, data in (("places", seed.PLACES), ("hotels", seed.HOTELS), ("cafes", seed.CAFES)):
            if c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0:
                cols = COLUMNS[table]
                c.executemany(
                    f"INSERT INTO {table}({','.join(cols)}) VALUES({','.join('?'*len(cols))})",
                    [tuple(r.get(k) for k in cols) for r in data])
        c.commit()
    finally:
        c.close()


def rows(table, where="", params=()):
    c = conn()
    try:
        return [dict(r) for r in c.execute(f"SELECT * FROM {table} {where}", params).fetchall()]
    finally:
        c.close()


def _run(sql, params=()):
    c = conn()
    try:
        c.execute(sql, params)
        c.commit()
    finally:
        c.close()


def insert(table, data):
    cols = [k for k in COLUMNS[table] if k in data]
    _run(f"INSERT INTO {table}({','.join(cols)}) VALUES({','.join('?'*len(cols))})", [data[k] for k in cols])


def update(table, rid, data):
    cols = [k for k in COLUMNS[table] if k in data]
    _run(f"UPDATE {table} SET {','.join(k+'=?' for k in cols)} WHERE id=?", [data[k] for k in cols] + [rid])


def delete(table, rid):
    _run(f"DELETE FROM {table} WHERE id=?", (rid,))


def log_chat(username, q, a):
    _run("INSERT INTO chat_log(username,question,answer) VALUES(?,?,?)", (username, q, a))


# ---------- auth ----------
def register(username, full_name, email, password):
    username = username.strip().lower()
    if len(username) < 3 or len(password) < 6:
        return False, "Username needs 3+ characters and password needs 6+ characters."
    h, s = hash_pw(password)
    try:
        _run("INSERT INTO users(username,full_name,email,pw_hash,salt,role) VALUES(?,?,?,?,?,'tourist')",
             (username, full_name.strip(), email.strip(), h, s))
        return True, "Account created. You can log in now."
    except sqlite3.IntegrityError:
        return False, "That username is already taken."


def login(username, password):
    u = rows("users", "WHERE username=?", (username.strip().lower(),))
    if not u:
        return None
    u = u[0]
    h, _ = hash_pw(password, u["salt"])
    return u if hmac.compare_digest(h, u["pw_hash"]) else None
