"""
UZBHackHub — friendly fallback for photos / voice / video / documents / stickers.
Photos sent while in note-taking mode are handled by handlers.notes instead.
"""
import logging

from telegram import Update
from telegram.ext import ContextTypes

from localization import t
from handlers.helpers import get_lang

log = logging.getLogger(__name__)


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    lang = get_lang(uid)
    msg = update.message

    if msg.photo:
        await msg.reply_text(t(lang, "media_photo"))
    elif msg.voice or msg.audio or msg.video_note:
        await msg.reply_text(t(lang, "media_voice"))
    elif msg.document:
        await msg.reply_text(t(lang, "media_doc"))
    else:
        await msg.reply_text(t(lang, "media_other"))
