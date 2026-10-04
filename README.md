# 🛡️ UZBHackHub — Cybersecurity Learning Bot for Telegram

A professional, bilingual (**English 🇬🇧 / O'zbekcha 🇺🇿**) Telegram bot that teaches
cybersecurity through interactive lessons and quizzes, with user accounts, XP,
levels, daily streaks, personal notes, and reminders — and a clean path to
future monetization (Premium section already wired in).

Built with **Python 3.10+** and **python-telegram-bot v21** (async) + SQLite.

---

## ✨ Features

| Area | What you get |
|------|--------------|
| 🔐 **Lessons** | 3 modules × 2 lessons (passwords, phishing, malware, Wi-Fi/VPN safety), fully bilingual |
| 📝 **Quizzes** | 3 questions per lesson, shuffled options, instant feedback with explanations |
| 🏆 **Gamification** | XP per correct answer, completion bonuses, 5 levels (Novice → Legend), daily streaks |
| 👤 **User accounts** | Auto-registered in SQLite: language, XP, streak, lesson progress |
| 📝 **Notes** | Personal notes in text *or photo* form, list & delete with inline buttons |
| ⏰ **Reminders** | `/remind 30m text` or guided flow with duration buttons; survives bot restarts |
| 🌐 **Bilingual** | English + Uzbek everywhere, switchable via /lang or Settings |
| ⭐ **Premium-ready** | Placeholder Premium section — ready for your monetization plans |

## 📁 Project structure

```
uzbhackhub_bot/
├── bot.py               # entry point: wiring, handlers, commands
├── config.py            # token loading, XP settings, limits
├── database.py          # SQLite layer (users, progress, notes, reminders)
├── localization.py      # all EN/UZ strings
├── keyboards.py         # inline keyboards
├── content/
│   └── lessons.py       # lesson & quiz content  ← add your lessons here
├── handlers/
│   ├── common.py        # /start /menu /help /profile /lang /premium
│   ├── lessons.py       # lesson browser + quiz engine
│   ├── notes.py         # notes (text + photo)
│   ├── reminders.py     # reminder engine (JobQueue)
│   ├── media.py         # photo/voice/document fallback
│   └── helpers.py       # levels, progress bar, sanitizers
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## 🚀 Quick start (local test)

```bash
cd uzbhackhub_bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then paste your token into .env
python bot.py
```

Open Telegram, find your bot, press **Start** — done. ✅

## ☁️ Deploy to Railway (24/7, free tier friendly)

1. Create a new GitHub repository and push this folder.
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**.
3. In your service → **Variables** → add:
   ```
   BOT_TOKEN = 123456:ABC-your-token
   ```
4. Railway auto-detects the `Dockerfile` (or Python) and starts the bot.
5. Check **Deployments → Logs** — you should see
   `UZBHackHub bot is up and running 🚀`

> 💡 Railway gives your container persistent disk only if you attach a Volume.
> Attach a Volume mounted at `/app/data` so the SQLite DB survives restarts.

## 🖥️ Deploy to a VPS (Ubuntu + systemd)

```bash
sudo apt update && sudo apt install -y python3-venv
git clone <your-repo> uzbhackhub && cd uzbhackhub
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env        # paste token

sudo tee /etc/systemd/system/uzbhackhub.service > /dev/null <<EOF
[Unit]
Description=UZBHackHub Telegram bot
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now uzbhackhub
journalctl -u uzbhackhub -f        # watch logs
```

Docker alternative: `docker build -t uzbhackhub . && docker run -d --env-file .env -v $(pwd)/data:/app/data uzbhackhub`

## ➕ Adding your own lessons

Open `content/lessons.py`, copy any lesson dict, and translate it:

```python
{
    "id": "net1",                    # unique id
    "title_en": "Network Basics", "title_uz": "Tarmoq asoslari",
    "body_en":  "...lesson text, *markdown* allowed...",
    "body_uz":  "...",
    "quiz": [
        {
            "q_en": "...", "q_uz": "...",
            "opts_en": ["A","B","C","D"], "opts_uz": [...],
            "correct": 2,            # index of the right option (0-based)
            "explain_en": "...", "explain_uz": "...",
        },
    ],
}
```

Everything else (progress, XP, quizzes, menus) updates automatically.

## 🧭 Bot commands

| Command | Action |
|---------|--------|
| `/start` | Main menu / first-time language picker |
| `/menu` | Main menu |
| `/lessons` | Jump straight to lessons |
| `/notes` | Your notes |
| `/remind 30m text` | Reminder in 30 minutes (`m`/`h`/`d` supported) |
| `/profile` | XP, level, streak, progress |
| `/lang` | Switch EN ⇄ UZ |
| `/premium` | Premium section (monetization-ready) |
| `/cancel` | Abort note/reminder input |

## 🔐 Good practices baked in

- Token loaded from environment/`.env` — never hardcoded, `.gitignore` protects it
- User input sanitized before being echoed into Markdown messages
- Photo attachments stored outside the database, referenced by path
- Reminders persisted in SQLite and re-scheduled on restart
- Non-root Docker user; database lives in `data/` (easy to mount as a Volume)

## 💰 Monetization roadmap (Premium section)

The Premium screen is already a wired-up placeholder. Natural next steps:

1. **Payments** — Telegram Stars (`XTR`) or Payments API for one-time unlock
2. **Gated content** — extra modules visible only to paying users (check a `is_premium` column)
3. **Certificates** — auto-generated PDFs at 100% course completion
4. **Referral system** — invite friends for bonus XP

Ready for your ideas — the architecture keeps user data separate from content,
so adding paid tiers is a small, safe change.
