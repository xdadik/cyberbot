"""
UZBHackHub — inline keyboards.
Callback data scheme:
  menu:<section>            main menu navigation
  setlang:<lang>            language switch
  module:<module_id>        open module lesson list
  lesson:view:<id>          open lesson text
  lesson:quiz:<id>          start quiz
  lesson:q:<lid>:<qi>:<oi>  quiz answer
  note:add / note:list / note:del:<id> / note:cancel
  rem:list / rem:cancel:<id> / rem:dur:<minutes>
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from content.lessons import MODULES, get_module_by_lesson, next_lesson
from localization import t


def lang_selection() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🇬🇧 English", callback_data="setlang:en"),
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="setlang:uz"),
        ]]
    )


def main_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "btn_lessons"), callback_data="menu:lessons"),
                InlineKeyboardButton(t(lang, "btn_notes"), callback_data="menu:notes"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_reminders"), callback_data="menu:reminders"),
                InlineKeyboardButton(t(lang, "btn_profile"), callback_data="menu:profile"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_settings"), callback_data="menu:settings"),
                InlineKeyboardButton(t(lang, "btn_premium"), callback_data="menu:premium"),
            ],
        ]
    )


def settings_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "btn_lang"), callback_data="menu:lang")],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:main")],
        ]
    )


def back_to_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")]]
    )


def modules_menu(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for mod in MODULES:
        rows.append([
            InlineKeyboardButton(
                f"{mod['icon']} {mod['title_en'] if lang == 'en' else mod['title_uz']}",
                callback_data=f"module:{mod['id']}",
            )
        ])
    rows.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def module_menu(lang: str, module_id: str, completed: set[str]) -> InlineKeyboardMarkup:
    mod = next((m for m in MODULES if m["id"] == module_id), None)
    rows = []
    if mod:
        for les in mod["lessons"]:
            mark = t(lang, "lesson_status_done") if les["id"] in completed else t(lang, "lesson_status_open")
            title = les["title_en"] if lang == "en" else les["title_uz"]
            rows.append([
                InlineKeyboardButton(f"{mark} {title}", callback_data=f"lesson:view:{les['id']}")
            ])
    rows.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:lessons")])
    rows.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def lesson_menu(lang: str, lesson_id: str) -> InlineKeyboardMarkup:
    mod = get_module_by_lesson(lesson_id)
    mid = mod["id"] if mod else ""
    rows = [
        [InlineKeyboardButton(t(lang, "btn_start_quiz"), callback_data=f"lesson:quiz:{lesson_id}")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data=f"module:{mid}")],
        [InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")],
    ]
    return InlineKeyboardMarkup(rows)


def quiz_options(lang: str, lesson_id: str, q_idx: int, quiz: list[dict]) -> InlineKeyboardMarkup:
    q = quiz[q_idx]
    opts = q["opts_en"] if lang == "en" else q["opts_uz"]
    rows = []
    for i, opt in enumerate(opts):
        rows.append([
            InlineKeyboardButton(
                f"{'ABCD'[i]}. {opt}",
                callback_data=f"lesson:q:{lesson_id}:{q_idx}:{i}",
            )
        ])
    rows.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def quiz_finished_menu(lang: str, lesson_id: str) -> InlineKeyboardMarkup:
    nxt = next_lesson(lesson_id)
    rows = []
    if nxt:
        title = nxt["title_en"] if lang == "en" else nxt["title_uz"]
        rows.append([
            InlineKeyboardButton(f"{t(lang, 'btn_next_lesson')} {title}", callback_data=f"lesson:view:{nxt['id']}")
        ])
    rows.append([
        InlineKeyboardButton(t(lang, "btn_retry_quiz"), callback_data=f"lesson:quiz:{lesson_id}")
    ])
    rows.append([InlineKeyboardButton(t(lang, "btn_lessons"), callback_data="menu:lessons")])
    rows.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def notes_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "btn_add_note"), callback_data="note:add")],
            [InlineKeyboardButton(t(lang, "btn_my_notes"), callback_data="note:list")],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:main")],
        ]
    )


def notes_list(lang: str, notes) -> InlineKeyboardMarkup:
    rows = []
    for n in notes:
        text = (n["text"] or "🖼 photo").strip().replace("\n", " ")
        if len(text) > 28:
            text = text[:28] + "…"
        rows.append([
            InlineKeyboardButton(f"📄 {text}", callback_data="noop"),
            InlineKeyboardButton(t(lang, "btn_delete"), callback_data=f"note:del:{n['id']}"),
        ])
    rows.append([InlineKeyboardButton(t(lang, "btn_add_note"), callback_data="note:add")])
    rows.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:notes")])
    return InlineKeyboardMarkup(rows)


def reminders_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "btn_rem_list"), callback_data="rem:list")],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:main")],
        ]
    )


def reminder_durations(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "btn_rem_10m"), callback_data="rem:dur:10"),
                InlineKeyboardButton(t(lang, "btn_rem_30m"), callback_data="rem:dur:30"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_rem_1h"), callback_data="rem:dur:60"),
                InlineKeyboardButton(t(lang, "btn_rem_3h"), callback_data="rem:dur:180"),
            ],
            [InlineKeyboardButton(t(lang, "btn_rem_1d"), callback_data="rem:dur:1440")],
            [InlineKeyboardButton(t(lang, "btn_rem_custom"), callback_data="rem:custom")],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:reminders")],
        ]
    )


def reminders_list(lang: str, reminders) -> InlineKeyboardMarkup:
    rows = []
    for r in reminders:
        text = r["text"].strip().replace("\n", " ")
        if len(text) > 24:
            text = text[:24] + "…"
        rows.append([
            InlineKeyboardButton(f"⏰ {text}", callback_data="noop"),
            InlineKeyboardButton("✖️", callback_data=f"rem:cancel:{r['id']}"),
        ])
    rows.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:reminders")])
    return InlineKeyboardMarkup(rows)


# ------------------------------------------------------------------ admin --

def admin_panel(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "btn_adm_stats"), callback_data="adm:stats"),
                InlineKeyboardButton(t(lang, "btn_adm_users"), callback_data="adm:users"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_adm_broadcast"), callback_data="adm:broadcast"),
                InlineKeyboardButton(t(lang, "btn_adm_vip"), callback_data="adm:vip"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_adm_payments"), callback_data="adm:payments"),
            ],
        ]
    )


def admin_user_actions(lang: str, uid: int, is_vip: bool, banned: bool) -> InlineKeyboardMarkup:
    vip_btn = (
        InlineKeyboardButton(t(lang, "btn_adm_viprevoke"), callback_data=f"adm:revoke:{uid}")
        if is_vip
        else InlineKeyboardButton(t(lang, "btn_adm_vipgrant"), callback_data=f"adm:grant:{uid}")
    )
    ban_btn = (
        InlineKeyboardButton(t(lang, "btn_adm_unban"), callback_data=f"adm:unban:{uid}")
        if banned
        else InlineKeyboardButton(t(lang, "btn_adm_ban"), callback_data=f"adm:ban:{uid}")
    )
    return InlineKeyboardMarkup(
        [
            [vip_btn],
            [ban_btn],
            [InlineKeyboardButton(t(lang, "btn_adm_users"), callback_data="adm:users"),
             InlineKeyboardButton(t(lang, "btn_adm_back"), callback_data="adm:panel")],
        ]
    )


def admin_back(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "btn_adm_back"), callback_data="adm:panel")]]
    )


# -------------------------------------------------------------------- vip --

def premium_menu(lang: str, price: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                t(lang, "btn_buy_vip", price=price), callback_data="vip:buy"
            )],
            [InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu:main")],
        ]
    )
