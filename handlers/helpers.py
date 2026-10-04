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
