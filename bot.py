"""
UZBHackHub — Telegram bot entry point.
Run:  python bot.py
"""
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import common, lessons, media, notes, reminders

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("uzbhackhub")


async def post_init(application: Application) -> None:
    """Set the command menu and restore pending reminders after a restart."""
    await application.bot.set_my_commands(
        [
            ("start", "Main menu / Asosiy menyu"),
            ("lessons", "Cybersecurity lessons"),
            ("notes", "Your notes"),
            ("remind", "Set a reminder: /remind 30m text"),
            ("profile", "Your stats"),
            ("lang", "Switch language (EN/UZ)"),
            ("premium", "Premium plans"),
            ("help", "How to use the bot"),
        ]
    )
    reminders.reschedule_pending(application)
    log.info("UZBHackHub bot is up and running 🚀")


def main() -> None:
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # ------------------------------------------------------------ commands --
    application.add_handler(CommandHandler("start", common.start))
    application.add_handler(CommandHandler("menu", common.menu_command))
    application.add_handler(CommandHandler("help", common.help_command))
    application.add_handler(CommandHandler("profile", common.profile))
    application.add_handler(CommandHandler("lang", common.lang_command))
    application.add_handler(CommandHandler("premium", common.premium))
    application.add_handler(CommandHandler("lessons", lessons_command))
    application.add_handler(CommandHandler("notes", notes_command))
    application.add_handler(CommandHandler("remind", reminders.remind_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    # ---------------------------------------------------- callback queries --
    application.add_handler(CallbackQueryHandler(common.set_language, pattern=r"^setlang:(en|uz)$"))
    application.add_handler(CallbackQueryHandler(lessons.show_lessons, pattern=r"^menu:lessons$"))
    application.add_handler(CallbackQueryHandler(lessons.show_module, pattern=r"^module:([A-Za-z0-9_]+)$"))
    application.add_handler(CallbackQueryHandler(lessons.view_lesson, pattern=r"^lesson:view:([A-Za-z0-9_]+)$"))
    application.add_handler(CallbackQueryHandler(lessons.start_quiz, pattern=r"^lesson:quiz:([A-Za-z0-9_]+)$"))
    application.add_handler(CallbackQueryHandler(lessons.answer_question,
                                                 pattern=r"^lesson:q:([A-Za-z0-9_]+):(\d+):(\d+)$"))
    application.add_handler(CallbackQueryHandler(notes.add_note_start, pattern=r"^note:add$"))
    application.add_handler(CallbackQueryHandler(notes.list_notes, pattern=r"^note:list$"))
    application.add_handler(CallbackQueryHandler(notes.delete_note, pattern=r"^note:del:(\d+)$"))
    application.add_handler(CallbackQueryHandler(notes.cancel_mode, pattern=r"^note:cancel$"))
    application.add_handler(CallbackQueryHandler(reminders.list_reminders, pattern=r"^rem:list$"))
    application.add_handler(CallbackQueryHandler(reminders.cancel_reminder, pattern=r"^rem:cancel:(\d+)$"))
    application.add_handler(CallbackQueryHandler(reminders.pick_duration, pattern=r"^rem:dur:(\d+)$"))
    application.add_handler(CallbackQueryHandler(reminders.ask_custom_duration, pattern=r"^rem:custom$"))
    application.add_handler(CallbackQueryHandler(common.show_settings, pattern=r"^menu:settings$"))
    application.add_handler(CallbackQueryHandler(common.show_lang_picker, pattern=r"^menu:lang$"))
    application.add_handler(CallbackQueryHandler(common.show_profile, pattern=r"^menu:profile$"))
    application.add_handler(CallbackQueryHandler(common.show_premium, pattern=r"^menu:premium$"))
    application.add_handler(CallbackQueryHandler(common.show_help, pattern=r"^menu:help$"))
    application.add_handler(CallbackQueryHandler(common.show_main_menu, pattern=r"^menu:main$"))
    application.add_handler(CallbackQueryHandler(common.noop, pattern=r"^noop$"))

    # ------------------------------------------------------------- messages --
    # 1) Photos: become note attachments when the user is adding a note.
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.PHOTO, notes.capture_note_photo
    ))
    # 2) Plain text: notes / reminder drafts, otherwise ignored.
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, route_text
    ))
    # 3) Any other media in private chat: friendly fallback.
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE
        & (filters.VOICE | filters.AUDIO | filters.VIDEO | filters.VIDEO_NOTE
           | filters.Document.ALL | filters.Sticker.ALL),
        media.handle_media,
    ))

    application.add_error_handler(common.error_handler)

    log.info("Starting UZBHackHub bot…")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# --------------------------------------------------------------- adapters --
# Small shims so /lessons, /notes and /cancel reuse the callback logic.
async def lessons_command(update: Update, context) -> None:
    import database as _db
    from localization import t as _t
    from handlers.helpers import get_lang as _gl
    from content.lessons import TOTAL_LESSONS as _TOTAL
    from keyboards import modules_menu as _mm

    uid = update.effective_user.id
    lang = _gl(uid)
    done = len(_db.get_progress(uid))
    await update.effective_message.reply_text(
        _t(lang, "lessons_title", done=done, total=_TOTAL),
        parse_mode="Markdown",
        reply_markup=_mm(lang),
    )


async def notes_command(update: Update, context) -> None:
    import database as _db
    from localization import t as _t
    from handlers.helpers import get_lang as _gl
    from config import MAX_NOTES
    from keyboards import notes_menu as _nm

    uid = update.effective_user.id
    lang = _gl(uid)
    count = _db.count_notes(uid)
    await update.effective_message.reply_text(
        _t(lang, "notes_menu", count=count, max=MAX_NOTES),
        parse_mode="Markdown",
        reply_markup=_nm(lang),
    )


async def cancel_command(update: Update, context) -> None:
    from handlers.helpers import get_lang as _gl
    from localization import t as _t

    lang = _gl(update.effective_user.id)
    context.user_data.pop("mode", None)
    context.user_data.pop("rem_draft", None)
    await update.effective_message.reply_text(_t(lang, "note_cancelled"))


async def route_text(update: Update, context) -> None:
    """Notes draft → reminder draft → nothing."""
    if await notes.capture_note_text(update, context):
        return
    if await reminders.capture_reminder_text(update, context):
        return
    # Idle chat: a gentle nudge instead of silence.
    from handlers.helpers import get_lang as _gl
    from localization import t as _t

    lang = _gl(update.effective_user.id)
    await update.message.reply_text(_t(lang, "media_other"))


if __name__ == "__main__":
    main()
