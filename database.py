"""
UZBHackHub — SQLite database layer.
Simple synchronous sqlite3 wrapper (fast enough for a learning bot),
thread-safe via a lock.
"""
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

from config import DATA_DIR, DEFAULT_LANG

DB_PATH = DATA_DIR / "uzbhackhub.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.RLock()  # reentrant: some helpers call other locked helpers
_conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL;")
        _init_schema(_conn)
    return _conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY,
            username     TEXT,
            first_name   TEXT,
            lang         TEXT DEFAULT 'en',
            xp           INTEGER DEFAULT 0,
            streak       INTEGER DEFAULT 1,
            last_active  TEXT,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS progress (
            user_id      INTEGER NOT NULL,
            lesson_id    TEXT NOT NULL,
            score        INTEGER DEFAULT 0,
            total        INTEGER DEFAULT 0,
            completed_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, lesson_id)
        );

        CREATE TABLE IF NOT EXISTS notes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            text         TEXT DEFAULT '',
            media_file   TEXT,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            text         TEXT NOT NULL,
            remind_at    TEXT NOT NULL,
            done         INTEGER DEFAULT 0,
            created_at   TEXT DEFAULT (datetime('now'))
        );
        """
    )
    conn.commit()


# ------------------------------------------------------------------ users --

def upsert_user(tg_user) -> sqlite3.Row:
    """Insert user if new; refresh name/username. Returns the row."""
    with _lock:
        conn = get_conn()
        conn.execute(
            """
            INSERT INTO users (id, username, first_name, lang, last_active)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username   = excluded.username,
                first_name = excluded.first_name,
                last_active = excluded.last_active
            """,
            (
                tg_user.id,
                tg_user.username or "",
                tg_user.first_name or "",
                DEFAULT_LANG,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        return get_user(tg_user.id)


def get_user(uid: int) -> sqlite3.Row | None:
    with _lock:
        row = get_conn().execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    return row


def set_lang(uid: int, lang: str) -> None:
    with _lock:
        conn = get_conn()
        conn.execute("UPDATE users SET lang = ? WHERE id = ?", (lang, uid))
        conn.commit()


def add_xp(uid: int, amount: int) -> int:
    """Add XP, return the user's new total."""
    with _lock:
        conn = get_conn()
        conn.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, uid))
        conn.commit()
        row = conn.execute("SELECT xp FROM users WHERE id = ?", (uid,)).fetchone()
    return row["xp"] if row else 0


def touch_streak(uid: int) -> int:
    """Update daily streak. Returns current streak count."""
    now = datetime.now(timezone.utc)
    with _lock:
        conn = get_conn()
        row = conn.execute(
            "SELECT last_active, streak FROM users WHERE id = ?", (uid,)
        ).fetchone()
        if not row:
            return 1
        streak = row["streak"] or 1
        last = row["last_active"]
        if last:
            try:
                last_dt = datetime.fromisoformat(last)
            except ValueError:
                last_dt = None
            if last_dt:
                delta_days = (now.date() - last_dt.date()).days
                if delta_days == 0:
                    conn.execute(
                        "UPDATE users SET last_active = ? WHERE id = ?",
                        (now.isoformat(timespec="seconds"), uid),
                    )
                    conn.commit()
                    return streak
                streak = streak + 1 if delta_days == 1 else 1
        conn.execute(
            "UPDATE users SET streak = ?, last_active = ? WHERE id = ?",
            (streak, now.isoformat(timespec="seconds"), uid),
        )
        conn.commit()
    return streak


# --------------------------------------------------------------- progress --

def mark_lesson_done(uid: int, lesson_id: str, score: int, total: int) -> None:
    with _lock:
        conn = get_conn()
        conn.execute(
            """
            INSERT INTO progress (user_id, lesson_id, score, total)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, lesson_id) DO UPDATE SET
                score = MAX(score, excluded.score),
                completed_at = datetime('now')
            """,
            (uid, lesson_id, score, total),
        )
        conn.commit()


def get_progress(uid: int) -> dict[str, sqlite3.Row]:
    """Map of lesson_id -> progress row for the user."""
    with _lock:
        rows = get_conn().execute(
            "SELECT * FROM progress WHERE user_id = ?", (uid,)
        ).fetchall()
    return {r["lesson_id"]: r for r in rows}


# ------------------------------------------------------------------ notes --

def add_note(uid: int, text: str, media_file: str | None = None) -> int:
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO notes (user_id, text, media_file) VALUES (?, ?, ?)",
            (uid, text, media_file),
        )
        conn.commit()
    return cur.lastrowid


def list_notes(uid: int, limit: int = 10) -> list[sqlite3.Row]:
    with _lock:
        rows = get_conn().execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (uid, limit),
        ).fetchall()
    return rows


def count_notes(uid: int) -> int:
    with _lock:
        row = get_conn().execute(
            "SELECT COUNT(*) AS c FROM notes WHERE user_id = ?", (uid,)
        ).fetchone()
    return row["c"] if row else 0


def delete_note(uid: int, note_id: int) -> bool:
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, uid)
        )
        conn.commit()
    return cur.rowcount > 0


# -------------------------------------------------------------- reminders --

def add_reminder(uid: int, text: str, remind_at: datetime) -> int:
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)",
            (uid, text, remind_at.isoformat(timespec="seconds")),
        )
        conn.commit()
    return cur.lastrowid


def list_reminders(uid: int) -> list[sqlite3.Row]:
    with _lock:
        rows = get_conn().execute(
            "SELECT * FROM reminders WHERE user_id = ? AND done = 0 ORDER BY remind_at",
            (uid,),
        ).fetchall()
    return rows


def count_reminders(uid: int) -> int:
    with _lock:
        row = get_conn().execute(
            "SELECT COUNT(*) AS c FROM reminders WHERE user_id = ? AND done = 0",
            (uid,),
        ).fetchone()
    return row["c"] if row else 0


def cancel_reminder(uid: int, rid: int) -> bool:
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ? AND done = 0",
            (rid, uid),
        )
        conn.commit()
    return cur.rowcount > 0


def get_reminder(rid: int) -> sqlite3.Row | None:
    with _lock:
        row = get_conn().execute(
            "SELECT * FROM reminders WHERE id = ?", (rid,)
        ).fetchone()
    return row


def mark_reminder_done(rid: int) -> None:
    with _lock:
        conn = get_conn()
        conn.execute("UPDATE reminders SET done = 1 WHERE id = ?", (rid,))
        conn.commit()


def get_pending_reminders() -> list[sqlite3.Row]:
    """All unfinished reminders (used on startup to re-schedule jobs)."""
    with _lock:
        rows = get_conn().execute(
            "SELECT * FROM reminders WHERE done = 0"
        ).fetchall()
    return rows


# ---------------------------------------------------------------- utility --

def parse_duration(text: str) -> timedelta | None:
    """Parse '30m', '2h', '1d' into timedelta. Returns None if invalid."""
    text = text.strip().lower()
    if len(text) < 2 or not text[:-1].isdigit() or text[-1] not in "mhd":
        return None
    amount = int(text[:-1])
    unit = text[-1]
    if unit == "m":
        return timedelta(minutes=amount)
    if unit == "h":
        return timedelta(hours=amount)
    return timedelta(days=amount)
