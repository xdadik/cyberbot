"""
UZBHackHub — configuration module.
Loads the bot token from environment variables or a local .env file.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ATTACH_DIR = DATA_DIR / "attachments"
ATTACH_DIR.mkdir(parents=True, exist_ok=True)


def _load_dotenv(path: Path) -> None:
    """Tiny .env loader (no external dependency needed)."""
    env_file = path / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv(BASE_DIR)

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "\n" + "=" * 60 + "\n"
        "  BOT_TOKEN is missing!\n\n"
        "  1. Open @BotFather in Telegram and send /mybots\n"
        "  2. Copy your bot token (looks like 123456:ABC-xyz...)\n"
        "  3. Either:\n"
        "     - put it in a .env file:  BOT_TOKEN=123456:ABC-xyz...\n"
        "     - or export it:           export BOT_TOKEN=123456:ABC-xyz...\n"
        + "=" * 60
    )

# ---------------------------------------------------------------------------
# Gamification settings
# ---------------------------------------------------------------------------
XP_PER_CORRECT = 10        # XP for each correct quiz answer (first attempt only)
XP_PER_LESSON = 30         # bonus XP for finishing a lesson the first time
XP_PER_LEVEL = 100         # XP needed per level

LEVELS = [
    (1, "Novice", "Yangichoq"),
    (2, "Defender", "Himoyachi"),
    (3, "Guardian", "Qo'riqchi"),
    (4, "Hacker Pro", "Pro Xaker"),
    (5, "Legend", "Afsona"),
]

MAX_NOTE_LEN = 3500        # max characters per note
MAX_NOTES = 30             # max notes stored per user
MAX_REMINDERS = 10         # max active reminders per user

DEFAULT_LANG = "en"
SUPPORTED_LANGS = ("en", "uz")
