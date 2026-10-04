"""
UZBHackHub — lessons & quiz engine with XP, levels and progress tracking.

Quiz state (context.user_data["quiz"]) looks like:
    {
        "lesson_id":  "pw1",
        "q_idx":      0,                      # current question index
        "score":      0,
        "first_time": True,                   # XP awarded only on first pass
        "order_map":  {0: [2,0,3,1], ...}     # display order -> original index
    }
Callback data for answers carries the ORIGINAL option index, so scoring is
independent of display order:  lesson:q:<lesson_id>:<q_idx>:<orig_idx>
"""
import logging
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database as db
from config import XP_PER_CORRECT, XP_PER_LESSON
from content.lessons import MODULES, TOTAL_LESSONS, get_lesson, get_module_by_lesson
from keyboards import lesson_menu, modules_menu, module_menu, quiz_finished_menu
from localization import t
from handlers.helpers import get_lang, level_name, vip_multiplier

log = logging.getLogger(__name__)


async def show_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    done = len(db.get_progress(uid))
    await query.edit_message_text(
        t(lang, "lessons_title", done=done, total=TOTAL_LESSONS),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=modules_menu(lang),
    )


async def show_module(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    module_id = context.match.group(1)
    mod = next((m for m in MODULES if m["id"] == module_id), None)
    if not mod:
        await query.edit_message_text(t(lang, "err_lesson_not_found"))
        return
    completed = set(db.get_progress(uid).keys())
    done = sum(1 for l in mod["lessons"] if l["id"] in completed)
    title = mod["title_en"] if lang == "en" else mod["title_uz"]
    await query.edit_message_text(
        t(lang, "module_title", icon=mod["icon"], title=title,
          done=done, total=len(mod["lessons"])),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=module_menu(lang, module_id, completed),
    )


async def view_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    lesson_id = context.match.group(1)
    les = get_lesson(lesson_id)
    if not les:
        await query.edit_message_text(t(lang, "err_lesson_not_found"))
        return

    title = les["title_en"] if lang == "en" else les["title_uz"]
    body = les["body_en"] if lang == "en" else les["body_uz"]
    mod = get_module_by_lesson(lesson_id)
    completed = lesson_id in db.get_progress(uid)

    text = t(lang, "lesson_header", icon=mod["icon"] if mod else "🔐",
             title=title, body=body, tip=t(lang, "lesson_tip"))
    if completed:
        text += "\n\n" + t(lang, "lesson_completed_before")

    # Telegram hard limit is 4096 chars per message — split defensively.
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)]
    await query.edit_message_text(
        chunks[0], parse_mode=ParseMode.MARKDOWN,
        reply_markup=lesson_menu(lang, lesson_id),
    )
    for chunk in chunks[1:]:
        await context.bot.send_message(
            chat_id=query.message.chat_id, text=chunk, parse_mode=ParseMode.MARKDOWN
        )


# ---------------------------------------------------------------- quiz ----

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    lesson_id = context.match.group(1)
    les = get_lesson(lesson_id)
    if not les:
        await query.edit_message_text(t(lang, "err_lesson_not_found"))
        return

    order_map = {
        i: random.sample(range(len(q["opts_en"])), len(q["opts_en"]))
        for i, q in enumerate(les["quiz"])
    }
    context.user_data["quiz"] = {
        "lesson_id": lesson_id,
        "q_idx": 0,
        "score": 0,
        "first_time": lesson_id not in db.get_progress(uid),
        "order_map": order_map,
    }
    await _render_question(query, lang, les, 0, order_map[0])


async def _render_question(query, lang: str, les: dict, q_idx: int,
                           order: list[int], prefix: str = "") -> None:
    q = les["quiz"][q_idx]
    title = les["title_en"] if lang == "en" else les["title_uz"]
    question = q["q_en"] if lang == "en" else q["q_uz"]
    opts = q["opts_en"] if lang == "en" else q["opts_uz"]

    rows = []
    for pos, orig in enumerate(order):
        rows.append([
            InlineKeyboardButton(
                f"{'ABCD'[pos]}. {opts[orig]}",
                callback_data=f"lesson:q:{les['id']}:{q_idx}:{orig}",
            )
        ])
    rows.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")])

    await query.edit_message_text(
        prefix + t(lang, "quiz_question", lesson=title, n=q_idx + 1,
                   total=len(les["quiz"]), question=question),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)

    state = context.user_data.get("quiz")
    if not state:
        await query.edit_message_text(t(lang, "err_generic"))
        return

    lesson_id = context.match.group(1)
    q_idx = int(context.match.group(2))
    chosen = int(context.match.group(3))

    # Ignore stale clicks on already-answered questions.
    if lesson_id != state["lesson_id"] or q_idx != state["q_idx"]:
        return

    les = get_lesson(lesson_id)
    if not les or q_idx >= len(les["quiz"]):
        await query.edit_message_text(t(lang, "err_lesson_not_found"))
        return

    q = les["quiz"][q_idx]
    correct = q["correct"]
    opts = q["opts_en"] if lang == "en" else q["opts_uz"]
    explain = q["explain_en"] if lang == "en" else q["explain_uz"]

    is_right = chosen == correct
    gained = 0
    if is_right:
        state["score"] += 1
        if state.get("first_time"):
            gained = XP_PER_CORRECT * vip_multiplier(uid)
            db.add_xp(uid, gained)

    feedback = (
        t(lang, "quiz_correct", explain=explain) if is_right
        else t(lang, "quiz_wrong", answer=opts[correct], explain=explain)
    )
    if gained:
        feedback += t(lang, "quiz_xp_gain", xp=gained)

    nxt = q_idx + 1
    if nxt < len(les["quiz"]):
        state["q_idx"] = nxt
        prefix = feedback + "\n\n➖➖➖\n\n"
        await _render_question(
            query, lang, les, nxt, state["order_map"][nxt], prefix=prefix
        )
    else:
        await _finish_quiz(query, context, uid, lang, les, state, last_feedback=feedback)


async def _finish_quiz(query, context, uid: int, lang: str, les: dict,
                       state: dict, last_feedback: str) -> None:
    score = state["score"]
    total = len(les["quiz"])
    pct = round(score / total * 100) if total else 0
    lesson_id = les["id"]

    bonus_line = ""
    if state.get("first_time"):
        db.mark_lesson_done(uid, lesson_id, score, total)
        bonus = XP_PER_LESSON * vip_multiplier(uid)
        db.add_xp(uid, bonus)
        bonus_line = t(lang, "lesson_xp_bonus", xp=bonus)

    xp = db.get_user(uid)["xp"] or 0
    motivation = (
        t(lang, "quiz_motivation_high") if pct >= 80
        else t(lang, "quiz_motivation_mid") if pct >= 50
        else t(lang, "quiz_motivation_low")
    )
    body = (
        last_feedback
        + "\n\n➖➖➖\n\n"
        + t(lang, "quiz_finished", score=score, total=total, pct=pct,
            xp_line=bonus_line, xp=xp, level=1 + xp // 100,
            level_name=level_name(lang, xp), motivation=motivation)
    )
    context.user_data.pop("quiz", None)
    await query.edit_message_text(
        body, parse_mode=ParseMode.MARKDOWN,
        reply_markup=quiz_finished_menu(lang, lesson_id),
    )
