"""
UZBHackHub — personal notes: text notes + optional photo attachments.
A tiny state machine via context.user_data["mode"]:
    "note_text"  — waiting for the user's note text (or a photo)
"""
import logging
import time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database as db
from config import ATTACH_DIR, MAX_NOTES, MAX_NOTE_LEN
from keyboards import notes_list, notes_menu
from localization import t
from handlers.helpers import get_lang, md_clean

log = logging.getLogger(__name__)


async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    count = db.count_notes(uid)
    await query.edit_message_text(
        t(lang, "notes_menu", count=count, max=MAX_NOTES),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=notes_menu(lang),
    )


async def add_note_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    context.user_data["mode"] = "note_text"
    await query.edit_message_text(
        t(lang, "note_prompt", cancel_cmd="cancel"),
        parse_mode=ParseMode.MARKDOWN,
    )


async def cancel_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    context.user_data.pop("mode", None)
    context.user_data.pop("rem_draft", None)
    count = db.count_notes(uid)
    await query.edit_message_text(
        t(lang, "note_cancelled") + "\n\n" + t(lang, "notes_menu", count=count, max=MAX_NOTES),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=notes_menu(lang),
    )


async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    notes = db.list_notes(uid)
    if not notes:
        await query.edit_message_text(
            t(lang, "notes_empty"), parse_mode=ParseMode.MARKDOWN,
            reply_markup=notes_menu(lang),
        )
        return
    await query.edit_message_text(
        t(lang, "btn_my_notes"), reply_markup=notes_list(lang, notes)
    )


async def delete_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    note_id = int(context.match.group(1))
    db.delete_note(uid, note_id)
    notes = db.list_notes(uid)
    if not notes:
        await query.edit_message_text(
            t(lang, "note_deleted") + "\n\n" + t(lang, "notes_empty"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=notes_menu(lang),
        )
        return
    await query.edit_message_text(
        t(lang, "note_deleted") + "\n\n" + t(lang, "btn_my_notes"),
        reply_markup=notes_list(lang, notes),
    )


async def capture_note_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """If the bot is in note-taking mode, save this text as a note.
    Returns True when the message was consumed."""
    if context.user_data.get("mode") != "note_text":
        return False
    uid = update.effective_user.id
    lang = get_lang(uid)

    text = update.message.text or ""
    if len(text) > MAX_NOTE_LEN or db.count_notes(uid) >= MAX_NOTES:
        await update.message.reply_text(
            t(lang, "note_limit", max=MAX_NOTE_LEN, max_notes=MAX_NOTES)
        )
        return True

    safe = md_clean(text) or "…"
    db.add_note(uid, safe)
    context.user_data.pop("mode", None)
    await update.message.reply_text(
        t(lang, "note_added", text=safe[:200]),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=notes_menu(lang),
    )
    return True


async def capture_note_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Photo sent while in note mode → save as a photo note."""
    uid = update.effective_user.id
    lang = get_lang(uid)
    in_note_mode = context.user_data.get("mode") == "note_text"

    if not in_note_mode:
        await update.message.reply_text(t(lang, "media_photo"))
        return

    if db.count_notes(uid) >= MAX_NOTES:
        await update.message.reply_text(t(lang, "note_limit", max=MAX_NOTE_LEN, max_notes=MAX_NOTES))
        context.user_data.pop("mode", None)
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    path = ATTACH_DIR / f"{uid}_{int(time.time())}.jpg"
    await file.download_to_drive(str(path))

    caption = md_clean(update.message.caption or "")
    db.add_note(uid, caption or "🖼 photo", media_file=str(path))
    context.user_data.pop("mode", None)
    await update.message.reply_text(
        t(lang, "note_photo_added"), reply_markup=notes_menu(lang)
    )
