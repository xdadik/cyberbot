"""
UZBHackHub — bilingual localization (English / Uzbek).
Usage:  t(lang, "key", **kwargs)
"""

STRINGS = {
    # ------------------------------------------------------------- generic --
    "en": {
        "choose_lang": "🌐 *Choose your language / Tilni tanlang:*",
        "lang_changed": "✅ Language set to *English*.",
        "welcome_new": "👋 Hello, *{name}*!\n\nWelcome to *UZBHackHub* 🛡️\nYour personal cybersecurity academy inside Telegram:\n\n• 🔐 Interactive lessons & quizzes\n• 📝 Personal notes\n• ⏰ Reminders\n• 🏆 XP, levels and streaks\n\nChoose your language:",
        "welcome_back": "👋 Welcome back, *{name}*!\n\n🔥 Streak: *{streak} day(s)*  •  ⭐ XP: *{xp}*  •  🎖 Level {level} — *{level_name}*\n\nWhat do you want to do today?",
        "main_menu": "🏠 *Main Menu*\n\nChoose a section:",
        "btn_lessons": "🔐 Lessons",
        "btn_notes": "📝 Notes",
        "btn_reminders": "⏰ Reminders",
        "btn_profile": "👤 Profile",
        "btn_settings": "⚙️ Settings",
        "btn_premium": "⭐ Premium",
        "btn_help": "❓ Help",
        "btn_back": "◀️ Back",
        "btn_menu": "🏠 Menu",
        "btn_lang": "🌐 Language",
        "btn_start_quiz": "📝 Take the quiz",
        "btn_retry_quiz": "🔁 Retake quiz",
        "btn_next_lesson": "➡️ Next lesson",
        "help_text": (
            "❓ *UZBHackHub — Help*\n\n"
            "*Commands:*\n"
            "/start — open the main menu\n"
            "/menu — main menu\n"
            "/lessons — cybersecurity lessons\n"
            "/notes — your notes\n"
            "/remind — set a reminder: `/remind 30m Buy milk`\n"
            "/profile — your stats\n"
            "/lang — switch language (EN/UZ)\n"
            "/premium — premium plans\n\n"
            "*How it works:*\n"
            "📖 Study a lesson → 📝 take the quiz → earn ⭐ XP and level up!\n"
            "Come back every day to keep your 🔥 streak alive.\n\n"
            "💡 Tip: you can also send me a *photo* while adding a note — it will be attached automatically."
        ),
        "profile_text": (
            "👤 *Your Profile*\n\n"
            "🆔 ID: `{uid}`\n"
            "📛 Name: *{name}*\n"
            "🌐 Language: *{lang}*\n\n"
            "⭐ XP: *{xp}*\n"
            "🎖 Level {level} — *{level_name}*\n"
            "🔥 Streak: *{streak} day(s)*\n"
            "📚 Lessons completed: *{done}/{total}*\n"
            "{bar}"
        ),
        "premium_text": (
            "⭐ *UZBHackHub Premium — coming soon!*\n\n"
            "We are preparing exclusive perks for our best students:\n\n"
            "• 🧠 Advanced hacking labs & challenges\n"
            "• 📜 Personal certificates\n"
            "• 🚫 Zero ads, priority support\n"
            "• 👥 Private community access\n\n"
            "💰 Follow our channel to be the first to know when Premium launches.\n"
            "_Your learning data is already saved — Premium will simply unlock more._"
        ),
        "settings_text": "⚙️ *Settings*\n\nCurrent language: *{lang}*\n\nTap to change:",
        # ---------------------------------------------------------- lessons --
        "lessons_title": "🔐 *Cybersecurity Lessons*\n\nTotal progress: *{done}/{total}* lessons completed\n\nPick a module:",
        "module_title": "{icon} *{title}*\n\nCompleted: *{done}/{total}*\n\nChoose a lesson:",
        "lesson_status_done": "✅",
        "lesson_status_open": "▶️",
        "lesson_header": "{icon} *{title}*\n\n{body}\n\n_{tip}_",
        "lesson_tip": "Read carefully — the quiz is next! 👀",
        "lesson_completed_before": "♻️ You already completed this lesson — a retake gives no extra XP, but let's see what you remember!",
        "quiz_question": "📝 *Quiz* — {lesson}\n\n*Question {n}/{total}:*\n\n{question}",
        "quiz_correct": "✅ *Correct!* {explain}",
        "quiz_wrong": "❌ *Wrong.* Correct answer: *{answer}*. {explain}",
        "quiz_xp_gain": "\n\n⭐ +{xp} XP",
        "quiz_finished": (
            "🏁 *Quiz finished!*\n\n"
            "📊 Score: *{score}/{total}* ({pct}%)\n"
            "{xp_line}\n"
            "🎖 Level {level} — *{level_name}* ({xp} XP)\n\n"
            "{motivation}"
        ),
        "quiz_motivation_high": "🔥 Excellent work, hacker!",
        "quiz_motivation_mid": "👍 Good job — review and try again for a perfect score!",
        "quiz_motivation_low": "💪 Don't give up — reread the lesson and try again!",
        "lesson_xp_bonus": "🎁 +{xp} bonus XP for completing the lesson!",
        "err_lesson_not_found": "⚠️ Lesson not found. Open /lessons again.",
        # ------------------------------------------------------------ notes --
        "notes_menu": "📝 *Notes*\n\nSave your own cybersecurity cheat-sheets, passwords hints (never real passwords! 🙈), or anything else.\n\nStored: *{count}/{max}*",
        "notes_empty": "📭 You have no notes yet.\n\nTap *➕ Add note* and send me any text!",
        "note_added": "✅ Note saved!\n\n💬 \"{text}\"\n\nFind it anytime in 📝 Notes.",
        "note_photo_added": "📸 Photo note saved! You can view the file in the bot's data folder.",
        "note_prompt": "✍️ Send me the text of your note now (or a photo).\n\n/{cancel_cmd} to abort.",
        "note_limit": "⚠️ Note is too long (max {max} characters) or you reached the {max_notes}-note limit.",
        "note_deleted": "🗑 Note deleted.",
        "note_cancelled": "↩️ Cancelled.",
        "btn_add_note": "➕ Add note",
        "btn_my_notes": "📚 My notes",
        "btn_delete": "🗑",
        # -------------------------------------------------------- reminders --
        "reminders_menu": "⏰ *Reminders*\n\nNever miss your daily security practice!\n\n*Quick way:*\n`/remind 30m Review phishing lesson`\n\n*Or:* send me the text first — I'll ask for the time.\n\nActive reminders: *{count}/{max}*",
        "rem_prompt_text": "✍️ What should I remind you about?",
        "rem_prompt_time": "⏰ In how long? Choose below or type like `45m`, `2h`, `1d`.",
        "rem_set": "✅ Reminder set: *\"{text}\"* — I'll ping you {when}.\n(⏰ {at})",
        "rem_list_empty": "📭 No active reminders.\n\nCreate one: `/remind 1h Practice SQL`",
        "rem_list_title": "⏰ *Your active reminders:*",
        "rem_item": "• {text}\n  ⏰ {at}",
        "rem_cancelled": "🗑 Reminder cancelled.",
        "rem_fired": "⏰ *Reminder!*\n\n💬 {text}\n\n_Stay consistent — your future self says thanks!_ 🛡️",
        "rem_invalid": "⚠️ I couldn't understand the time. Use formats like `30m`, `2h`, `1d` and a text:\n`/remind 30m Check email headers`",
        "rem_limit": "⚠️ You reached the {max}-reminder limit. Cancel one first.",
        "rem_too_soon": "⚠️ Minimum reminder time is 5 minutes.",
        "btn_rem_10m": "10 min",
        "btn_rem_30m": "30 min",
        "btn_rem_1h": "1 hour",
        "btn_rem_3h": "3 hours",
        "btn_rem_1d": "1 day",
        "btn_rem_custom": "✍️ Custom",
        "btn_rem_list": "📋 My reminders",
        # -------------------------------------------------------------- media --
        "media_photo": "📸 Cool screenshot! If you want to *save it as a note*, tap 📝 Notes → ➕ Add note and send it again.",
        "media_voice": "🎙 Voice message received! Voice transcription is coming in a future update — meanwhile, type me your question. 😊",
        "media_doc": "📄 File received! For security reasons I don't open files — but I appreciate the trust! 😄",
        "media_other": "🤖 Got it! I'm mainly a lessons & notes bot — try /menu to see everything I can do.",
        # -------------------------------------------------------------- errors --
        "err_generic": "😥 Something went wrong. Please try again or use /menu.",
        "err_not_registered": "👋 Please /start the bot first!",
    },

    # ------------------------------------------------------------- uzbek --
    "uz": {
        "choose_lang": "🌐 *Tilni tanlang / Choose your language:*",
        "lang_changed": "✅ Til *o'zbekcha* ga o'zgartirildi.",
        "welcome_new": "👋 Salom, *{name}*!\n\n*UZBHackHub* botiga xush kelibsiz! 🛡️\nTelegram ichidagi shaxsiy kiberxavfsizlik akademiyangiz:\n\n• 🔐 Interaktiv darslar va kvizlar\n• 📝 Shaxsiy eslatmalar\n• ⏰ Eslatqilar (remind)\n• 🏆 XP, darajalar va streak\n\nTilni tanlang:",
        "welcome_back": "👋 Yana xush kelibsiz, *{name}*!\n\n🔥 Streak: *{streak} kun*  •  ⭐ XP: *{xp}*  •  🎖 {level}-daraja — *{level_name}*\n\nBugun nima qilamiz?",
        "main_menu": "🏠 *Asosiy menyu*\n\nBo'limni tanlang:",
        "btn_lessons": "🔐 Darslar",
        "btn_notes": "📝 Eslatmalar",
        "btn_reminders": "⏰ Eslatqilar",
        "btn_profile": "👤 Profil",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_premium": "⭐ Premium",
        "btn_help": "❓ Yordam",
        "btn_back": "◀️ Orqaga",
        "btn_menu": "🏠 Menyu",
        "btn_lang": "🌐 Til",
        "btn_start_quiz": "📝 Kvizni boshlash",
        "btn_retry_quiz": "🔁 Qayta ishlash",
        "btn_next_lesson": "➡️ Keyingi dars",
        "help_text": (
            "❓ *UZBHackHub — Yordam*\n\n"
            "*Buyruqlar:*\n"
            "/start — asosiy menyu\n"
            "/menu — asosiy menyu\n"
            "/lessons — kiberxavfsizlik darslari\n"
            "/notes — eslatmalaringiz\n"
            "/remind — eslatqa o'rnatish: `/remind 30m Sut olish`\n"
            "/profile — statistikangiz\n"
            "/lang — tilni almashtirish (EN/UZ)\n"
            "/premium — premium rejalar\n\n"
            "*Qanday ishlaydi:*\n"
            "📖 Darsni o'qing → 📝 kvizni topshiring → ⭐ XP yig'ib darajangizni oshiring!\n"
            "Har kuni keling — 🔥 streak saqlansin.\n\n"
            "💡 Maslahat: eslatma qo'shayotganda *rasm* ham yuborishingiz mumkin — avtomatik ilova qilinadi."
        ),
        "profile_text": (
            "👤 *Profilingingiz*\n\n"
            "🆔 ID: `{uid}`\n"
            "📛 Ism: *{name}*\n"
            "🌐 Til: *{lang}*\n\n"
            "⭐ XP: *{xp}*\n"
            "🎖 {level}-daraja — *{level_name}*\n"
            "🔥 Streak: *{streak} kun*\n"
            "📚 Tugallangan darslar: *{done}/{total}*\n"
            "{bar}"
        ),
        "premium_text": (
            "⭐ *UZBHackHub Premium — tez orada!*\n\n"
            "Eng yaxshi o'quvchilarimiz uchun maxsus imkoniyatlar tayyorlanyapti:\n\n"
            "• 🧠 Kengaytirilgan hacking laboratoriyalari\n"
            "• 📜 Shaxsiy sertifikatlar\n"
            "• 🚫 Reklamasiz, ustuvor yordam\n"
            "• 👥 Maxfiy hamjamiyatga kirish\n\n"
            "💰 Premium ishga tushganda birinchi bo'lib bilish uchun kanalimizga a'zo bo'ling.\n"
            "_O'quv natijalaringiz allaqachon saqlanadi — Premium ularni faqat kengaytiradi._"
        ),
        "settings_text": "⚙️ *Sozlamalar*\n\nJoriy til: *{lang}*\n\nO'zgartirish uchun bosing:",
        # ---------------------------------------------------------- lessons --
        "lessons_title": "🔐 *Kiberxavfsizlik darslari*\n\nUmumiy progress: *{done}/{total}* dars tugallangan\n\nModulni tanlang:",
        "module_title": "{icon} *{title}*\n\nTugallangan: *{done}/{total}*\n\nDarsni tanlang:",
        "lesson_status_done": "✅",
        "lesson_status_open": "▶️",
        "lesson_header": "{icon} *{title}*\n\n{body}\n\n_{tip}_",
        "lesson_tip": "Diqqat bilan o'qing — endi kviz bor! 👀",
        "lesson_completed_before": "♻️ Bu darsni allaqachon tugallgansiz — qayta ishlash XP bermaydi, lekin eslab qolganingizni tekshiramiz!",
        "quiz_question": "📝 *Kviz* — {lesson}\n\n*Savol {n}/{total}:*\n\n{question}",
        "quiz_correct": "✅ *To'g'ri!* {explain}",
        "quiz_wrong": "❌ *Noto'g'ri.* To'g'ri javob: *{answer}*. {explain}",
        "quiz_xp_gain": "\n\n⭐ +{xp} XP",
        "quiz_finished": (
            "🏁 *Kviz tugadi!*\n\n"
            "📊 Natija: *{score}/{total}* ({pct}%)\n"
            "{xp_line}\n"
            "🎖 {level}-daraja — *{level_name}* ({xp} XP)\n\n"
            "{motivation}"
        ),
        "quiz_motivation_high": "🔥 Zo'r ish, xaker!",
        "quiz_motivation_mid": "👍 Yaxshi! Takrorlab, to'liq natija uchun yana urinib ko'ring!",
        "quiz_motivation_low": "💪 Taslim bo'lmang — darsni qayta o'qing va yana urining!",
        "lesson_xp_bonus": "🎁 Darsni tugallagani uchun +{xp} bonus XP!",
        "err_lesson_not_found": "⚠️ Dars topilmadi. /lessons ni qayta oching.",
        # ------------------------------------------------------------ notes --
        "notes_menu": "📝 *Eslatmalar*\n\nKiberxavfsizlik bo'yicha o'z chevar malumotlaringizni saqlang (haqiqiy parollarni emas! 🙈).\n\nSaqlangan: *{count}/{max}*",
        "notes_empty": "📭 Hozircha eslatmangiz yo'q.\n\n*➕ Eslatma qo'shish* tugmasini bosing va matn yuboring!",
        "note_added": "✅ Eslatma saqlandi!\n\n💬 \"{text}\"\n\nXohlagan vaqtda 📝 Eslatmalar bo'limida topasiz.",
        "note_photo_added": "📸 Rasm eslatma sifatida saqlandi!",
        "note_prompt": "✍️ Eslatma matnini yuboring (yoki rasm).\n\nBekor qilish: /{cancel_cmd}",
        "note_limit": "⚠️ Eslatma juda uzun (maks {max} belgi) yoki {max_notes} ta chegaraikka yetdingiz.",
        "note_deleted": "🗑 Eslatma o'chirildi.",
        "note_cancelled": "↩️ Bekor qilindi.",
        "btn_add_note": "➕ Eslatma qo'shish",
        "btn_my_notes": "📚 Eslatmalarim",
        "btn_delete": "🗑",
        # -------------------------------------------------------- reminders --
        "reminders_menu": "⏰ *Eslatqilar*\n\nKundalik mashg'ulotlaringizni unutmang!\n\n*Tezkor usul:*\n`/remind 30m Phishing darsini takrorlash`\n\n*Yoki:* avval matn yuboring — vaqtni so'raymiz.\n\nFaol eslatqilar: *{count}/{max}*",
        "rem_prompt_text": "✍️ Nima haqida eslatma beray?",
        "rem_prompt_time": "⏰ Qanchadan keyin? Pastdan tanlang yoki `45m`, `2h`, `1d` deb yozing.",
        "rem_set": "✅ Eslatqa o'rnatildi: *\"{text}\"* — {when} eslataman.\n(⏰ {at})",
        "rem_list_empty": "📭 Faol eslatqa yo'q.\n\nYaratish: `/remind 1h SQL mashq`",
        "rem_list_title": "⏰ *Faol eslatqilaringiz:*",
        "rem_item": "• {text}\n  ⏰ {at}",
        "rem_cancelled": "🗑 Eslatqa bekor qilindi.",
        "rem_fired": "⏰ *Eslatqa!*\n\n💬 {text}\n\n_Barqaror bo'ling — kelajagingizdagi o'zingiz rahmat aytaydi!_ 🛡️",
        "rem_invalid": "⚠️ Vaqtni tushunmadim. `30m`, `2h`, `1d` kabi yozing va matn qo'shing:\n`/remind 30m Email tekshirish`",
        "rem_limit": "⚠️ {max} ta eslatqa chegaraikka yetdingiz. Avval birini bekor qiling.",
        "rem_too_soon": "⚠️ Eng kam vaqt — 5 daqiqa.",
        "btn_rem_10m": "10 daqiqa",
        "btn_rem_30m": "30 daqiqa",
        "btn_rem_1h": "1 soat",
        "btn_rem_3h": "3 soat",
        "btn_rem_1d": "1 kun",
        "btn_rem_custom": "✍️ Boshqa",
        "btn_rem_list": "📋 Eslatqilarim",
        # -------------------------------------------------------------- media --
        "media_photo": "📸 Yaxshi skrinshot! Uni *eslatma sifatida saqlash* uchun: 📝 Eslatmalar → ➕ qo'shish → rasmni qayta yuboring.",
        "media_voice": "🎙 Ovozli xabar qabul qilindi! Ovozni matnga aylantirish keyingi yangilanishlarda — hozircha savolingizni yozib yuboring. 😊",
        "media_doc": "📄 Fayl qabul qilindi! Xavfsizlik uchun fayllarni ochmayman — ishonchingiz uchun rahmat! 😄",
        "media_other": "🤖 Qabul qilindi! Men asosan darslar va eslatmalar botiman — /menu ni ochib ko'ring.",
        # -------------------------------------------------------------- errors --
        "err_generic": "😥 Xatolik yuz berdi. Qayta urinib ko'ring yoki /menu ni oching.",
        "err_not_registered": "👋 Avval botga /start bering!",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Translate a key with optional {placeholders}."""
    lang = lang if lang in STRINGS else "en"
    table = STRINGS[lang]
    text = table.get(key) or STRINGS["en"].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def lang_display(lang: str) -> str:
    return {"en": "English 🇬🇧", "uz": "O'zbekcha 🇺🇿"}.get(lang, lang)
