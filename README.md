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
| 🛡️ **Admin panel** | Password-protected `/admin`: stats, user cards, ban/unban, VIP grants, broadcast, payments |
| 💎 **VIP monetization** | Real payments with **Telegram Stars**, auto-expiry, 2× XP perk, VIP badge |

## 📁 Project structure

```
uzbhackhub_bot/
├── bot.py               # entry point: wiring, handlers, commands
├── config.py            # token loading, admin, VIP, XP settings, limits
├── database.py          # SQLite layer (users, progress, notes, reminders, payments)
├── localization.py      # all EN/UZ strings
├── keyboards.py         # inline keyboards (user + admin + VIP)
├── content/
│   └── lessons.py       # lesson & quiz content  ← add your lessons here
├── handlers/
│   ├── common.py        # /start /menu /help /profile /lang
│   ├── lessons.py       # lesson browser + quiz engine
│   ├── notes.py         # notes (text + photo)
│   ├── reminders.py     # reminder engine (JobQueue)
│   ├── vip.py           # Telegram Stars payments + VIP fulfillment
│   ├── admin.py         # admin panel: stats, users, ban, broadcast
│   ├── media.py         # photo/voice/document fallback
│   └── helpers.py       # levels, ban guard, XP multiplier, sanitizers
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

cp .env.example .env            # then paste your token + admin settings into .env
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
| `/premium` | VIP plans + buy with Telegram Stars |
| `/cancel` | Abort note/reminder/admin input |
| `/admin` | 🛡️ Admin panel (password or ADMIN_IDS) |

## 🔐 Good practices baked in

- Token loaded from environment/`.env` — never hardcoded, `.gitignore` protects it
- User input sanitized before being echoed into Markdown messages
- Photo attachments stored outside the database, referenced by path
- Reminders persisted in SQLite and re-scheduled on restart
- Non-root Docker user; database lives in `data/` (easy to mount as a Volume)

## 🛡️ Admin panel

Send `/admin` in the bot. Access is granted by either:

1. **Password** — set `ADMIN_PASSWORD` in `.env` (default `uzbhack-admin` — change it!)
2. **Telegram ID** — add comma-separated IDs to `ADMIN_IDS` (no password needed)

Panel capabilities:

| Section | What it does |
|---------|--------------|
| 📊 Statistics | Total/new/active users, active VIP, banned, Stars revenue |
| 👥 Users | Recent users → tap for a card: XP, streak, VIP, ban status |
| 💎 VIP | Grant/revoke VIP per user; shows price/duration config |
| 🚫 Ban | Banned users are blocked at every entry point with a notice |
| 📣 Broadcast | Sends a Markdown message to all non-banned users with a delivery report |
| 💰 Payments | Last successful Stars payments + total revenue |

## 💎 VIP with Telegram Stars

1. In-bot: ⭐ Premium → **Buy VIP** → Telegram shows a Stars invoice
2. User pays → `successful_payment` → VIP granted automatically (`VIP_DAYS`, extends on repeat)
3. Perks while active: **2× XP** (`VIP_XP_MULTIPLIER`), 💎 badge in profile, status in the Premium panel
4. All payments are stored in SQLite (`payments` table) and visible in the admin panel

> ⚠️ Stars payments need **no payment provider** — but double-check that your bot
> has no Payments provider configured conflict and test with a small price first.
