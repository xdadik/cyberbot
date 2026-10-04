"""
UZBHackHub — common handlers:
/start, /menu, /help, /profile, /lang, /premium + language switch + menu router.
"""
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database as db
from config import MAX_NOTES, MAX_REMINDERS
from content.lessons import TOTAL_LESSONS
from keyboards import (
    back_to_menu,
    lang_selection,
    main_menu,
    settings_menu,
)
from localization import t, lang_display
from handlers.helpers import get_lang, level_name, md_clean, progress_bar

log = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    row = db.upsert_user(user)
    db.touch_streak(user.id)
    uid = user.id
    lang = row["lang"] or "en"
    name = md_clean(user.first_name) or "friend"

    if context.user_data.get("greeted"):
        xp = row["xp"] or 0
        streak = row["streak"] or 1
        await update.effective_message.reply_text(
            t(lang, "welcome_back", name=name, streak=streak, xp=xp,
              level=1 + xp // 100, level_name=level_name(lang, xp)),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu(lang),
        )
    else:
        # First launch: onboarding starts with language selection.
        context.user_data["greeted"] = True
        await update.effective_message.reply_text(
            t(lang, "welcome_new", name=name),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=lang_selection(),
        )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update.effective_user.id)
    await update.effective_message.reply_text(
        t(lang, "main_menu"), parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu(lang)
    )


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = context.match.group(1) if context.match else "en"
    if lang not in ("en", "uz"):
        lang = "en"
    db.set_lang(update.effective_user.id, lang)
    context.user_data["lang_chosen"] = True
    await query.edit_message_text(
        t(lang, "lang_changed"), parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu(lang)
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update.effective_user.id)
    row = db.get_user(update.effective_user.id)
    xp = row["xp"] or 0 if row else 0
    streak = row["streak"] or 1 if row else 1
    name = md_clean(update.effective_user.first_name) or "friend"
    await query.edit_message_text(
        t(lang, "welcome_back", name=name, streak=streak, xp=xp,
          level=1 + xp // 100, level_name=level_name(lang, xp)),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu(lang),
    )


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update.effective_user.id)
    await query.edit_message_text(
        t(lang, "settings_text", lang=lang_display(lang)),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=settings_menu(lang),
    )


async def show_lang_picker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update.effective_user.id)
    await query.edit_message_text(
        t(lang, "choose_lang"), parse_mode=ParseMode.MARKDOWN, reply_markup=lang_selection()
    )


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update.effective_user.id)
    await update.effective_message.reply_text(
        t(lang, "choose_lang"), parse_mode=ParseMode.MARKDOWN, reply_markup=lang_selection()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update.effective_user.id)
    await update.effective_message.reply_text(
        t(lang, "help_text"), parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu(lang)
    )


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update.effective_user.id)
    await query.edit_message_text(
        t(lang, "help_text"), parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu(lang)
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    lang = get_lang(uid)
    row = db.get_user(uid)
    if not row:
        await update.effective_message.reply_text(t(lang, "err_not_registered"))
        return
    progress = db.get_progress(uid)
    done = len(progress)
    xp = row["xp"] or 0
    await update.effective_message.reply_text(
        t(
            lang,
            "profile_text",
            uid=uid,
            name=md_clean(row["first_name"] or update.effective_user.first_name or "—"),
            lang=lang_display(row["lang"] or "en"),
            xp=xp,
            level=1 + xp // 100,
            level_name=level_name(lang, xp),
            streak=row["streak"] or 1,
            done=done,
            total=TOTAL_LESSONS,
            bar=progress_bar(done, TOTAL_LESSONS),
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu(lang),
    )


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    lang = get_lang(uid)
    row = db.get_user(uid)
    if not row:
        await query.edit_message_text(t(lang, "err_not_registered"))
        return
    progress = db.get_progress(uid)
    done = len(progress)
    xp = row["xp"] or 0
    await query.edit_message_text(
        t(
            lang,
            "profile_text",
            uid=uid,
            name=md_clean(row["first_name"] or update.effective_user.first_name or "—"),
            lang=lang_display(row["lang"] or "en"),
            xp=xp,
            level=1 + xp // 100,
            level_name=level_name(lang, xp),
            streak=row["streak"] or 1,
            done=done,
            total=TOTAL_LESSONS,
            bar=progress_bar(done, TOTAL_LESSONS),
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu(lang),
    )


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update.effective_user.id)
    await update.effective_message.reply_text(
        t(lang, "premium_text"), parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu(lang)
    )


async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update.effective_user.id)
    await query.edit_message_text(
        t(lang, "premium_text"), parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu(lang)
    )


async def noop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answer purely-visual buttons so the spinner stops."""
    await update.callback_query.answer()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("Exception while handling an update:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_message:
            lang = get_lang(update.effective_user.id) if update.effective_user else "en"
            await update.effective_message.reply_text(t(lang, "err_generic"))
    except Exception:  # pragma: no cover - never raise from the error handler
        pass


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update.effective_user.id)
    await update.effective_message.reply_text(
        t(lang, "err_generic"), reply_markup=back_to_menu(lang)
    )
