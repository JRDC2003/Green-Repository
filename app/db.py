import sqlite3
import datetime
from typing import List, Dict

DB_PATH = "devices.db"


def get_conn():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)


def init_db() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ip TEXT UNIQUE,
        online INTEGER DEFAULT 0,
        last_seen TEXT
    )
    """
    )
    conn.commit()
    conn.close()


def get_all_devices() -> List[Dict]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, ip, online, last_seen FROM devices")
    rows = c.fetchall()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "ip": r[2], "online": bool(r[3]), "last_seen": r[4]}
        for r in rows
    ]


def register_device(name: str, ip: str) -> None:
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    try:
        c.execute("INSERT INTO devices(name, ip, online, last_seen) VALUES (?, ?, 0, ?)", (name, ip, now))
    except sqlite3.IntegrityError:
        c.execute("UPDATE devices SET name=? WHERE ip=?", (name, ip))
    conn.commit()
    conn.close()


def update_device_status(device_id: int, online: bool) -> None:
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    c.execute("UPDATE devices SET online=?, last_seen=? WHERE id=?", (1 if online else 0, now, device_id))
    conn.commit()
    conn.close()
