"""Shared helper functions for handlers."""
import re

from config import LEVELS, XP_PER_LEVEL
from database import get_user


def get_lang(uid: int) -> str:
    row = get_user(uid)
    return (row["lang"] if row else "en") or "en"


def level_of(xp: int) -> int:
    return min(xp // XP_PER_LEVEL + 1, LEVELS[-1][0])


def level_info(xp: int) -> tuple[int, str, str]:
    """Return (level, name_en, name_uz) for a given XP."""
    lvl = level_of(xp)
    for num, en, uz in LEVELS:
        if num == lvl:
            return num, en, uz
    return LEVELS[0]


def level_name(lang: str, xp: int) -> str:
    _, en, uz = level_info(xp)
    return en if lang == "en" else uz


def progress_bar(done: int, total: int, width: int = 10) -> str:
    filled = round(done / total * width) if total else 0
    filled = min(max(filled, 0), width)
    return "█" * filled + "░" * (width - filled)


_MD_CHARS = re.compile(r"[*_`\[\]]")


def md_clean(text: str) -> str:
    """Strip Markdown control characters from user-provided content."""
    return _MD_CHARS.sub("", text or "").strip()


def fmt_date(iso: str | None) -> str:
    """Human-readable date (dd.mm.yyyy) from an ISO string; '—' if empty."""
    from datetime import datetime
    if not iso:
        return "—"
    try:
        return datetime.fromisoformat(iso).strftime("%d.%m.%Y")
    except ValueError:
        return "—"


def banned_guard(fn):
    """Decorator for user-facing handlers: block banned users everywhere."""
    import database as _db
    from localization import t as _t

    async def wrapper(update, context):
        uid = update.effective_user.id if update.effective_user else 0
        if _db.is_banned(uid):
            lang = get_lang(uid)
            msg = _t(lang, "user_banned_msg")
            try:
                if update.callback_query:
                    await update.callback_query.answer(msg, show_alert=True)
                elif update.effective_message:
                    await update.effective_message.reply_text(msg)
            except Exception:
                pass
            return
        await fn(update, context)

    return wrapper


def vip_multiplier(uid: int) -> int:
    """XP multiplier for the user (2x for active VIP)."""
    from database import get_user, vip_active

    from config import VIP_XP_MULTIPLIER
    return VIP_XP_MULTIPLIER if vip_active(get_user(uid)) else 1
