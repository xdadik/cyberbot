"""
UZBHackHub — admin panel: password gate, stats, user management (VIP/ban),
broadcast, payments overview.

Access: Telegram IDs listed in ADMIN_IDS env bypass the password;
everyone else must send ADMIN_PASSWORD once per session.

States via context.user_data["mode"]: "admin_pass", "broadcast".
"""
import logging
from datetime import datetime

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

import database as db
from config import ADMIN_IDS, ADMIN_PASSWORD, VIP_DAYS, VIP_PRICE_STARS, VIP_XP_MULTIPLIER
from keyboards import admin_back, admin_panel, admin_user_actions
from localization import t
from handlers.helpers import get_lang, md_clean

log = logging.getLogger(__name__)


def _is_admin(uid: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return uid in ADMIN_IDS or bool(context.user_data.get("admin_ok"))


def _fmt_date(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        return datetime.fromisoformat(iso).strftime("%d.%m.%Y")
    except ValueError:
        return "—"


# ------------------------------------------------------------------- gate --

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    lang = get_lang(uid)
    if _is_admin(uid, context):
        await update.effective_message.reply_text(
            t(lang, "admin_panel"), parse_mode=ParseMode.MARKDOWN,
            reply_markup=admin_panel(lang),
        )
        return
    context.user_data["mode"] = "admin_pass"
    await update.effective_message.reply_text(t(lang, "admin_ask_pass"))


async def capture_admin_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Returns True if the message was an admin-password attempt."""
    if context.user_data.get("mode") != "admin_pass":
        return False
    uid = update.effective_user.id
    lang = get_lang(uid)
    context.user_data.pop("mode", None)

    if update.message.text and update.message.text.strip() == ADMIN_PASSWORD:
        context.user_data["admin_ok"] = True
        await update.message.reply_text(
            t(lang, "admin_granted") + "\n\n" + t(lang, "admin_panel"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=admin_panel(lang),
        )
    else:
        await update.message.reply_text(t(lang, "admin_wrong_pass"))
    return True


async def guard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Callback guard: verify admin rights, answer the query. True = proceed."""
    query = update.callback_query
    uid = query.from_user.id
    if not _is_admin(uid, context):
        await query.answer(t(get_lang(uid), "admin_denied"), show_alert=True)
        return False
    await query.answer()
    return True


# ----------------------------------------------------------------- panels --

async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    lang = get_lang(update.callback_query.from_user.id)
    await update.callback_query.edit_message_text(
        t(lang, "admin_panel"), parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_panel(lang),
    )


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    lang = get_lang(update.callback_query.from_user.id)
    s = db.admin_stats()
    await update.callback_query.edit_message_text(
        t(lang, "adm_stats", **s), parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_back(lang),
    )


async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    users = db.recent_users(10)
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    rows = []
    for u in users:
        name = md_clean(u["first_name"] or str(u["id"]))[:16]
        badge = " 💎" if db.vip_active(u) else ""
        flag = " 🚫" if u["banned"] else ""
        rows.append([InlineKeyboardButton(
            f"{name}{badge}{flag}", callback_data=f"adm:user:{u['id']}"
        )])
    rows.append([InlineKeyboardButton(t(lang, "btn_adm_back"), callback_data="adm:panel")])
    await query.edit_message_text(
        t(lang, "adm_users_title"), parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def show_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    uid = int(context.match.group(1))
    row = db.get_user(uid)
    if not row:
        await query.edit_message_text(t(lang, "adm_user_not_found"))
        return
    vip = db.vip_active(row)
    text = t(
        lang, "adm_user_card",
        uid=uid,
        name=md_clean(row["first_name"] or "—"),
        username=row["username"] or "—",
        lang=row["lang"] or "en",
        xp=row["xp"] or 0,
        streak=row["streak"] or 1,
        vip=f"{_fmt_date(row['vip_until'])}" if vip else t(lang, "vip_no"),
        banned=("YES ⛔" if row["banned"] else "no"),
        created=_fmt_date(row["created_at"]),
    )
    await query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_user_actions(lang, uid, vip, bool(row["banned"])),
    )


async def grant_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    uid = int(context.match.group(1))
    until = db.set_vip(uid, VIP_DAYS)
    await query.edit_message_text(
        t(lang, "adm_vip_granted", until=_fmt_date(until)) + f"\n\n🆔 {uid}",
        reply_markup=admin_back(lang),
    )


async def revoke_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    uid = int(context.match.group(1))
    db.revoke_vip(uid)
    await query.edit_message_text(
        t(lang, "adm_vip_revoked") + f"\n\n🆔 {uid}", reply_markup=admin_back(lang)
    )


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    uid = int(context.match.group(1))
    db.set_banned(uid, True)
    try:  # kick them out of any open menus
        await context.bot.send_message(uid, t(get_lang(uid), "user_banned_msg"))
    except TelegramError:
        pass
    await query.edit_message_text(
        t(lang, "adm_banned") + f"\n\n🆔 {uid}", reply_markup=admin_back(lang)
    )


async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    uid = int(context.match.group(1))
    db.set_banned(uid, False)
    await query.edit_message_text(
        t(lang, "adm_unbanned") + f"\n\n🆔 {uid}", reply_markup=admin_back(lang)
    )


async def show_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    active = [u for u in db.all_user_ids(include_banned=True)
              if db.vip_active(db.get_user(u))]
    await query.edit_message_text(
        t(lang, "adm_vip_panel", price=VIP_PRICE_STARS, days=VIP_DAYS,
          mult=VIP_XP_MULTIPLIER, count=len(active)),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_back(lang),
    )


async def show_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    rows = db.list_payments(10)
    if not rows:
        await query.edit_message_text(
            t(lang, "adm_payments_empty"), parse_mode=ParseMode.MARKDOWN,
            reply_markup=admin_back(lang),
        )
        return
    items = "\n".join(
        t(lang, "adm_payment_item", uid=r["user_id"], amount=r["amount"],
          currency=r["currency"], at=_fmt_date(r["created_at"]))
        for r in rows
    )
    await query.edit_message_text(
        t(lang, "adm_payments", items=items), parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_back(lang),
    )


# -------------------------------------------------------------- broadcast --

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update, context):
        return
    lang = get_lang(update.callback_query.from_user.id)
    context.user_data["mode"] = "broadcast"
    count = len(db.all_user_ids(include_banned=False))
    await update.callback_query.edit_message_text(
        t(lang, "adm_broadcast_prompt", count=count), parse_mode=ParseMode.MARKDOWN,
    )


async def capture_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Returns True if the message was consumed as a broadcast."""
    if context.user_data.get("mode") != "broadcast":
        return False
    uid = update.effective_user.id
    lang = get_lang(uid)
    context.user_data.pop("mode", None)

    targets = db.all_user_ids(include_banned=False)
    ok = fail = 0
    text = update.message.text or ""
    for target in targets:
        try:
            await context.bot.send_message(target, text, parse_mode=ParseMode.MARKDOWN)
            ok += 1
        except TelegramError:
            fail += 1
    await update.message.reply_text(
        t(lang, "adm_broadcast_done", ok=ok, fail=fail),
        parse_mode=ParseMode.MARKDOWN,
    )
    return True
