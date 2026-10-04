"""
UZBHackHub — VIP subscriptions paid with Telegram Stars (XTR).

Flow: premium panel → "Buy VIP" → send_invoice (Stars) →
      PreCheckoutQuery approved → successful_payment → VIP granted.

Configure price/duration via env: VIP_PRICE_STARS, VIP_DAYS.
"""
import logging
from datetime import datetime, timezone

from telegram import LabeledPrice, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database as db
from config import VIP_DAYS, VIP_PRICE_STARS, VIP_XP_MULTIPLIER
from keyboards import premium_menu
from localization import t
from handlers.helpers import get_lang, md_clean

log = logging.getLogger(__name__)

PAYLOAD = f"vip_{VIP_DAYS}d"


def _fmt(until_iso: str) -> str:
    try:
        return datetime.fromisoformat(until_iso).strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return "—"


async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)

    row = db.get_user(uid)
    if db.vip_active(row):
        vip_line = t(lang, "vip_status_active", until=_fmt(row["vip_until"]))
    else:
        vip_line = t(lang, "vip_status_none")

    await query.edit_message_text(
        t(lang, "premium_text", mult=VIP_XP_MULTIPLIER,
          price=VIP_PRICE_STARS, days=VIP_DAYS, vip_line=vip_line),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=premium_menu(lang, VIP_PRICE_STARS),
    )


async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    lang = get_lang(uid)
    row = db.get_user(uid)
    vip_line = (
        t(lang, "vip_status_active", until=_fmt(row["vip_until"]))
        if row and db.vip_active(row) else t(lang, "vip_status_none")
    )
    await update.effective_message.reply_text(
        t(lang, "premium_text", mult=VIP_XP_MULTIPLIER,
          price=VIP_PRICE_STARS, days=VIP_DAYS, vip_line=vip_line),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=premium_menu(lang, VIP_PRICE_STARS),
    )


async def buy_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the Stars invoice."""
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    await context.bot.send_invoice(
        chat_id=uid,
        title=t(lang, "vip_invoice_title"),
        description=t(lang, "vip_invoice_desc", days=VIP_DAYS, mult=VIP_XP_MULTIPLIER),
        payload=PAYLOAD,
        provider_token="",           # empty = Telegram Stars
        currency="XTR",
        prices=[LabeledPrice(label=t(lang, "vip_invoice_title"), amount=VIP_PRICE_STARS)],
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Approve only our own payloads."""
    q = update.pre_checkout_query
    if q.payload == PAYLOAD:
        await q.answer(ok=True)
    else:
        await q.answer(ok=False, error_message=t(get_lang(q.from_user.id), "err_payment_failed"))


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fulfill the VIP purchase."""
    payment = update.message.successful_payment
    uid = update.effective_user.id
    lang = get_lang(uid)

    db.record_payment(
        uid,
        charge_id=payment.provider_payment_charge_id or "",
        amount=payment.total_amount,
        currency=payment.currency,
    )
    until = db.set_vip(uid, VIP_DAYS)
    log.info("VIP purchased by %s (%s %s) until %s", uid, payment.total_amount, payment.currency, until)

    await update.message.reply_text(
        t(lang, "vip_purchase_success", until=_fmt(until), mult=VIP_XP_MULTIPLIER),
        parse_mode=ParseMode.MARKDOWN,
    )
