import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "schoolbridge.db"


@contextmanager
def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init() -> None:
    with _db() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                grade TEXT
            );
            CREATE TABLE IF NOT EXISTS notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                child TEXT,
                text TEXT NOT NULL,
                summary TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice_id INTEGER NOT NULL,
                child TEXT,
                task TEXT NOT NULL,
                due TEXT,
                done INTEGER NOT NULL DEFAULT 0
            );
            """
        )


def get_setting(key: str, default: str | None = None) -> str | None:
    with _db() as c:
        row = c.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with _db() as c:
        c.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def add_child(name: str, grade: str | None) -> None:
    with _db() as c:
        c.execute(
            "INSERT INTO children (name, grade) VALUES (?, ?) "
            "ON CONFLICT(name) DO UPDATE SET grade = excluded.grade",
            (name, grade),
        )


def list_children() -> list[dict]:
    with _db() as c:
        return [dict(r) for r in c.execute("SELECT * FROM children ORDER BY name")]


def child_exists(name: str) -> bool:
    with _db() as c:
        return c.execute("SELECT 1 FROM children WHERE name = ?", (name,)).fetchone() is not None


def add_notice(child: str | None, text: str, summary: str, actions: list[dict]) -> int:
    with _db() as c:
        cur = c.execute(
            "INSERT INTO notices (created_at, child, text, summary) VALUES (?,?,?,?)",
            (_now(), child, text, summary),
        )
        notice_id = cur.lastrowid
        for a in actions:
            c.execute(
                "INSERT INTO actions (notice_id, child, task, due) VALUES (?,?,?,?)",
                (notice_id, child, a["task"], a["due"]),
            )
        return notice_id


def list_actions(only_open: bool = True) -> list[dict]:
    query = "SELECT id, notice_id, child, task, due, done FROM actions"
    if only_open:
        query += " WHERE done = 0"
    query += " ORDER BY due IS NULL, due, id"
    with _db() as c:
        return [dict(r) for r in c.execute(query)]


def complete_action(action_id: int) -> bool:
    with _db() as c:
        cur = c.execute("UPDATE actions SET done = 1 WHERE id = ?", (action_id,))
        return cur.rowcount > 0