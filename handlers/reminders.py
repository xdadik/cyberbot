"""
UZBHackHub — reminders powered by python-telegram-bot JobQueue.

Flow A (quick):   /remind 30m Buy milk
Flow B (guided):  /remind  → send text  → pick duration buttons
States via context.user_data["mode"]: "rem_text" (waiting for text)
                                       "rem_dur" (waiting for custom time)
"""
import logging
from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database as db
from config import MAX_REMINDERS
from keyboards import reminder_durations, reminders_list, reminders_menu
from localization import t
from handlers.helpers import get_lang, md_clean

log = logging.getLogger(__name__)

MIN_MINUTES = 5


async def show_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    count = db.count_reminders(uid)
    await query.edit_message_text(
        t(lang, "reminders_menu", count=count, max=MAX_REMINDERS),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reminders_menu(lang),
    )


def _fmt_local(dt: datetime) -> str:
    return dt.strftime("%d.%m %H:%M")


def _schedule(app, rid: int, uid: int, when: timedelta) -> None:
    app.job_queue.run_once(
        fire_reminder,
        when=when,
        name=f"rem_{rid}",
        data={"rid": rid, "uid": uid},
    )


async def fire_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """JobQueue callback — deliver the reminder (if it still exists)."""
    data = context.job.data
    row = db.get_reminder(data["rid"])
    if not row or row["done"]:
        return  # cancelled earlier
    lang = get_lang(row["user_id"])
    try:
        await context.bot.send_message(
            chat_id=row["user_id"],
            text=t(lang, "rem_fired", text=md_clean(row["text"])),
            parse_mode=ParseMode.MARKDOWN,
        )
    finally:
        db.mark_reminder_done(row["id"])


async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    lang = get_lang(uid)

    if context.args:
        # Quick form: /remind 30m text...
        duration = db.parse_duration(context.args[0])
        text = " ".join(context.args[1:]).strip()
        if not duration or not text:
            await update.message.reply_text(t(lang, "rem_invalid"))
            return
        await _create_reminder(update, context, uid, lang, text, duration)
        return

    # Guided form
    context.user_data["mode"] = "rem_text"
    await update.message.reply_text(t(lang, "rem_prompt_text"))


async def _create_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           uid: int, lang: str, text: str, delta: timedelta) -> None:
    seconds = delta.total_seconds()
    if seconds < MIN_MINUTES * 60:
        await update.message.reply_text(t(lang, "rem_too_soon"))
        return
    if db.count_reminders(uid) >= MAX_REMINDERS:
        await update.message.reply_text(t(lang, "rem_limit", max=MAX_REMINDERS))
        return

    remind_at = datetime.now(timezone.utc) + delta
    rid = db.add_reminder(uid, md_clean(text) or "…", remind_at)
    _schedule(context.application, rid, uid, delta)

    human = _humanize(delta, lang)
    await update.message.reply_text(
        t(lang, "rem_set", text=md_clean(text)[:200], when=human, at=_fmt_local(remind_at)),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reminders_menu(lang),
    )


def _humanize(delta: timedelta, lang: str) -> str:
    minutes = int(delta.total_seconds() // 60)
    if minutes < 60:
        return f"{minutes} min"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:g} h" if hours != int(hours) else f"{int(hours)} h"
    return f"{int(hours // 24)} d"


async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    rows = db.list_reminders(uid)
    if not rows:
        await query.edit_message_text(
            t(lang, "rem_list_empty"), parse_mode=ParseMode.MARKDOWN,
            reply_markup=reminders_menu(lang),
        )
        return
    items = "\n".join(
        t(lang, "rem_item", text=md_clean(r["text"])[:60], at=_fmt_local(datetime.fromisoformat(r["remind_at"])))
        for r in rows
    )
    await query.edit_message_text(
        t(lang, "rem_list_title") + "\n\n" + items,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reminders_list(lang, rows),
    )


async def cancel_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    rid = int(context.match.group(1))
    db.cancel_reminder(uid, rid)
    # Best effort: remove the scheduled job too.
    for job in context.job_queue.get_jobs_by_name(f"rem_{rid}"):
        job.schedule_removal()
    rows = db.list_reminders(uid)
    if not rows:
        await query.edit_message_text(
            t(lang, "rem_cancelled") + "\n\n" + t(lang, "rem_list_empty"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reminders_menu(lang),
        )
        return
    items = "\n".join(
        t(lang, "rem_item", text=md_clean(r["text"])[:60], at=_fmt_local(datetime.fromisoformat(r["remind_at"])))
        for r in rows
    )
    await query.edit_message_text(
        t(lang, "rem_cancelled") + "\n\n" + t(lang, "rem_list_title") + "\n\n" + items,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reminders_list(lang, rows),
    )


async def pick_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    minutes = int(context.match.group(1))
    text = context.user_data.pop("rem_draft", None)
    if not text:
        await query.edit_message_text(t(lang, "rem_prompt_text"))
        context.user_data["mode"] = "rem_text"
        return
    context.user_data.pop("mode", None)
    await _create_reminder(update, context, uid, lang, text, timedelta(minutes=minutes))


async def ask_custom_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    if not context.user_data.get("rem_draft"):
        await query.edit_message_text(t(lang, "rem_prompt_text"))
        context.user_data["mode"] = "rem_text"
        return
    context.user_data["mode"] = "rem_dur"
    await query.edit_message_text(t(lang, "rem_prompt_time"))


async def capture_reminder_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Plain text message while in a reminder mode. Returns True if consumed."""
    mode = context.user_data.get("mode")
    if mode not in ("rem_text", "rem_dur"):
        return False
    uid = update.effective_user.id
    lang = get_lang(uid)
    text = update.message.text or ""

    if mode == "rem_text":
        context.user_data["rem_draft"] = text
        context.user_data.pop("mode", None)
        await update.message.reply_text(
            t(lang, "rem_prompt_time"), reply_markup=reminder_durations(lang)
        )
        return True

    # rem_dur mode: custom duration like 45m / 2h / 1d
    delta = db.parse_duration(text)
    if not delta:
        await update.message.reply_text(t(lang, "rem_invalid"))
        return True
    draft = context.user_data.pop("rem_draft", None)
    context.user_data.pop("mode", None)
    if not draft:
        await update.message.reply_text(t(lang, "rem_prompt_text"))
        context.user_data["mode"] = "rem_text"
        return True
    await _create_reminder(update, context, uid, lang, draft, delta)
    return True


def reschedule_pending(application) -> None:
    """On startup, re-schedule reminders that are still pending."""
    now = datetime.now(timezone.utc)
    for row in db.get_pending_reminders():
        try:
            remind_at = datetime.fromisoformat(row["remind_at"])
        except (ValueError, TypeError):
            continue
        delta = (remind_at - now).total_seconds()
        application.job_queue.run_once(
            fire_reminder,
            when=max(delta, 1.0),
            name=f"rem_{row['id']}",
            data={"rid": row["id"], "uid": row["user_id"]},
        )
