"""
UZBHackHub — cybersecurity lesson content (bilingual EN/UZ).

To add new lessons: append a dict to the module's "lessons" list following
the same structure. The bot picks everything up automatically.
"""

MODULES = [
    # ================================================================ module 1
    {
        "id": "pw",
        "icon": "🔑",
        "title_en": "Password Security",
        "title_uz": "Parol xavfsizligi",
        "lessons": [
            {
                "id": "pw1",
                "title_en": "Strong Passwords",
                "title_uz": "Kuchli parollar",
                "body_en": (
                    "Your password is the front door to your digital life. A weak one — "
                    "like *123456* or *password* — can be cracked in *less than a second*.\n\n"
                    "What makes a password strong?\n"
                    "• At least *12–16 characters* (length beats complexity!)\n"
                    "• A mix of letters, digits and symbols\n"
                    "• *No personal info* — birthdays and pet names are public knowledge for attackers\n"
                    "• *Unique per account* — reusing one password means one leak opens ALL your doors\n\n"
                    "A good trick is the *passphrase*: pick 4–5 random words, e.g. "
                    "*Blue-Tiger-Pizza-Rocket!* — easy for you to remember, brutal for machines to guess.\n\n"
                    "Attackers use *brute force* (trying every combination) and *dictionary attacks* "
                    "(trying millions of common passwords). Length is your best armor: every extra "
                    "character multiplies cracking time enormously."
                ),
                "body_uz": (
                    "Parolingiz — raqamli hayotingizning old eshigi. *123456* yoki *password* "
                    "kabi zaif parol *bir soniyadan kam* vaqtda buziladi.\n\n"
                    "Kuchli parol qanday bo'ladi?\n"
                    "• Kamida *12–16 belgi* (uzunlik murakkablikdan muhimroq!)\n"
                    "• Harflar, raqamlar va belgilar aralashmasi\n"
                    "• *Shaxsiy ma'lumotsiz* — tug'ilgan kunlar va uy hayvonlari nomi hujumchilar uchun ochiq\n"
                    "• *Har akkauntga alohida* — bir parolni qayta ishlatish bitta sizish barcha eshiklaringizni ochadi\n\n"
                    "Yaxshi usul — *ibora-parol (passphrase)*: 4–5 ta tasodifiy so'z tanlang, masalan "
                    "*Moviy-Yo'lbars-Pitsa-Raketa!* — sizga eslab qolish oson, mashinalarga topish qiyin.\n\n"
                    "Hujumchilar *brute force* (barcha kombinatsiyalarni sinash) va *lug'at hujumlari* "
                    "(millionlab mashhur parollarni sinash) usullarini ishlatadi. Uzunlik — eng yaxshi "
                    "zirhingiz: har qo'shimcha belgi buzish vaqtini ko'p barobar oshiradi."
                ),
                "quiz": [
                    {
                        "q_en": "Which password is the strongest?",
                        "q_uz": "Qaysi parol eng kuchli?",
                        "opts_en": ["123456789", "Summer2024!", "Blue-Tiger-Pizza-Rocket!", "iloveyou"],
                        "opts_uz": ["123456789", "Yoz2024!", "Moviy-Yo'lbars-Pitsa-Raketa!", "sevamanisaningizni"],
                        "correct": 2,
                        "explain_en": "A long random passphrase is both memorable and extremely hard to brute-force.",
                        "explain_uz": "Uzun tasodifiy ibora-parol ham eslab qolish oson, ham brute-force bilan buzish juda qiyin.",
                    },
                    {
                        "q_en": "Why must you use a DIFFERENT password for every account?",
                        "q_uz": "Har akkauntga ALOHIDA parol ishlatish nima uchun shart?",
                        "opts_en": [
                            "It looks more professional",
                            "One leaked password would expose all your accounts",
                            "Websites demand it by law",
                            "To make passwords easier to remember",
                        ],
                        "opts_uz": [
                            "Ko'rkamroq ko'rinadi",
                            "Bitta parol sizilsa, barcha akkauntlaringiz ochiladi",
                            "Saytlar qonun bo'yicha talab qiladi",
                            "Parollarni eslab qolish osonlashadi",
                        ],
                        "correct": 1,
                        "explain_en": "This is called 'credential stuffing' — attackers try leaked passwords on your other accounts.",
                        "explain_uz": "Bunga 'credential stuffing' deyiladi — hujumchilar sizilgan parollarni boshqa akkauntlaringizda sinab ko'radi.",
                    },
                    {
                        "q_en": "What do attackers use to try millions of common passwords quickly?",
                        "q_uz": "Hujumchilar millionlab mashhur parollarni tez sinash uchun nimadan foydalanadi?",
                        "opts_en": ["Dictionary attacks", "Antivirus", "Firewall", "Two-factor auth"],
                        "opts_uz": ["Lug'at hujumlari", "Antivirus", "Fauol (Firewall)", "Ikki bosqichli tasdiqlash"],
                        "correct": 0,
                        "explain_en": "Dictionary attacks run through lists of millions of previously leaked passwords.",
                        "explain_uz": "Lug'at hujumlari avval sizilgan millionlab parollar ro'yxatini sinab ko'radi.",
                    },
                ],
            },
            {
                "id": "pw2",
                "title_en": "Password Managers & 2FA",
                "title_uz": "Parol menejerlari va 2FA",
                "body_en": (
                    "How can you remember 50 unique strong passwords? You don't have to — a "
                    "*password manager* does it for you.\n\n"
                    "A password manager (Bitwarden, KeePass, 1Password…) stores all your passwords "
                    "in an *encrypted vault* unlocked by ONE master password. It can also generate "
                    "random uncrackable passwords and autofill them, so *phishing sites can't trick "
                    "you* — the manager only fills in the real website.\n\n"
                    "The second shield is *2FA (Two-Factor Authentication)*: even if thieves steal "
                    "your password, they still need a second factor — a code from an app "
                    "(Google Authenticator, Authy), a hardware key (YubiKey), or a biometric.\n\n"
                    "⚠️ Avoid SMS codes when possible — SIM-swap attacks let criminals hijack your "
                    "number. An authenticator app is much safer than SMS."
                ),
                "body_uz": (
                    "50 ta alohida kuchli parolni qanday eslab qolasiz? Kerak emas — buni *parol "
                    "menejeri* siz uchun qiladi.\n\n"
                    "Parol menejeri (Bitwarden, KeePass, 1Password…) barcha parollaringizni bitta "
                    "*master parol* bilan ochiladigan *shifrlangan seyfda* saqlaydi. U tasodifii "
                    "buzib bo'lmaydigan parollar yaratadi va avtomatik to'ldiradi — shu sababli "
                    "*phishing saytlari aldash olmaydi*: menejer haqiqiy saytgaagina to'ldiradi.\n\n"
                    "Ikkinchi qalqon — *2FA (ikki bosqichli tasdiqlash)*: agar hujumchi parolingizni "
                    "o'girlasa ham, ikkinchi omil kerak bo'ladi — ilova kodi (Google Authenticator, "
                    "Authy), apparat kaliti (YubiKey) yoki biometriya.\n\n"
                    "⚠️ SMS kodlardan imkon qadar saqlaning — SIM-swap hujumlari bilan jinoyatchilar "
                    "raqamingizni o'zlashtirishi mumkin. Authenticator ilovasi SMS dan ancha xavfsiz."
                ),
                "quiz": [
                    {
                        "q_en": "How many passwords do you need to remember when using a password manager?",
                        "q_uz": "Parol menejeri ishlatganda nechta parolni eslab qolish kerak?",
                        "opts_en": ["All of them", "One — the master password", "Two", "None at all"],
                        "opts_uz": ["Hammasini", "Bittasini — master parolni", "Ikkitasini", "Hech birini"],
                        "correct": 1,
                        "explain_en": "The vault stores everything; you unlock it with one strong master password.",
                        "explain_uz": "Seyf hammasini saqlaydi; siz uni bitta kuchli master parol bilan ochasiz.",
                    },
                    {
                        "q_en": "What is the safest form of 2FA?",
                        "q_uz": "Eng xavfsiz 2FA turi qaysi?",
                        "opts_en": ["SMS codes", "Email codes", "Authenticator app / hardware key", "Security questions"],
                        "opts_uz": ["SMS kodlar", "Email kodlar", "Authenticator ilovasi / apparat kaliti", "Maxfiy savollar"],
                        "correct": 2,
                        "explain_en": "Apps and hardware keys can't be intercepted like SMS (SIM-swap) or read like email.",
                        "explain_uz": "Ilova va apparat kalitlarini SMS kabi ushlash (SIM-swap) yoki email kabi o'qish mumkin emas.",
                    },
                    {
                        "q_en": "Why does a password manager protect you from phishing?",
                        "q_uz": "Parol menejeri phishing'dan qanday himoya qiladi?",
                        "opts_en": [
                            "It blocks dangerous websites",
                            "It only autofills on the genuine website's domain",
                            "It reports phishing to the police",
                            "It changes your password daily",
                        ],
                        "opts_uz": [
                            "Xavfli saytlarni bloklaydi",
                            "Faqat haqiqiy sayt domenida avtomatik to'ldiradi",
                            "Phishing haqida politsiyaga xabar beradi",
                            "Parolingizni har kuni o'zgartiradi",
                        ],
                        "correct": 1,
                        "explain_en": "A fake site has a different domain, so the manager won't fill in your credentials.",
                        "explain_uz": "Soxta sayt domeni boshqacha, shuning uchun menejer ma'lumotlaringizni to'ldirmaydi.",
                    },
                ],
            },
        ],
    },
    # ================================================================ module 2
    {
        "id": "ph",
        "icon": "🎣",
        "title_en": "Phishing Awareness",
        "title_uz": "Phishing xavfidan himoya",
        "lessons": [
            {
                "id": "ph1",
                "title_en": "Spotting Phishing",
                "title_uz": "Phishing'ni aniqlash",
                "body_en": (
                    "*Phishing* is the #1 cyber attack in the world: fake messages that pretend to "
                    "be your bank, a delivery company, or even your boss — all to steal your "
                    "passwords or money.\n\n"
                    "Red flags 🚩:\n"
                    "• *Urgency* — \"Your account will be blocked in 24 hours!\"\n"
                    "• *Too good to be true* — \"You won an iPhone!\"\n"
                    "• *Strange sender* — support@paypa1-secure.xyz (that's a ONE, not an L!)\n"
                    "• *Generic greeting* — \"Dear Customer\" instead of your name\n"
                    "• *Links that lie* — hover before you click: the real domain hides after the last '/'\n\n"
                    "Golden rule: *never* enter passwords or card numbers through a link someone "
                    "sent you. Open the official app or type the site address yourself."
                ),
                "body_uz": (
                    "*Phishing* — dunyodagi 1-raqamli kiberhujum: bankingiz, yetkazib berish "
                    "kompaniyasi yoki hatto rahbaringiz nomidan yozadigan soxta xabarlar — hammasi "
                    "parollaringiz yoki pulingizni o'girlash uchun.\n\n"
                    "Xavf belgilari 🚩:\n"
                    "• *Shoshilinchlik* — \"Akkauntingiz 24 soatda bloklanadi!\"\n"
                    "• *Juda yaxshi bo'lib ko'ringan* — \"iPhone yutdingiz!\"\n"
                    "• *G'alati yuboruvchi* — support@paypa1-secure.xyz (bu RAQAM 1, harf L emas!)\n"
                    "• *Umumiy murojaat* — ismingiz o'rniga \"Hurmatli mijoz\"\n"
                    "• *Yolg'on havolalar* — bosishdan oldin tekshiring: haqiqiy domen oxirgi '/' dan keyin yashiringan\n\n"
                    "Oltin qoida: hech qachon yuborilgan havola orqali parol yoki karta raqamini "
                    "kiritmang. Rasmiy ilovani oching yoki sayt manzilini o'zingiz yozing."
                ),
                "quiz": [
                    {
                        "q_en": "Which message is most likely phishing?",
                        "q_uz": "Qaysi xabar phishing bo'lishi ehtimoli ko'p?",
                        "opts_en": [
                            "\"Your monthly bank statement is ready in the app\"",
                            "\"URGENT: verify your account in 24h or it will be deleted! bit.ly/xyz\"",
                            "\"Meeting moved to 3pm, see you there\"",
                            "\"Thanks for your order #1284\" from the official site",
                        ],
                        "opts_uz": [
                            "\"Oylik bank hisobingiz ilovada tayyor\"",
                            "\"SHOSHILINCH: akkauntni 24 soatda tasdiqlang yoki o'chiriladi! bit.ly/xyz\"",
                            "\"Uchrashuv 15:00 ga ko'chirildi, ko'rishguncha\"",
                            "\"Buyurtmangiz #1284 uchun rahmat\" rasmiy saytdan",
                        ],
                        "correct": 1,
                        "explain_en": "Urgency + short link + threat = classic phishing trio.",
                        "explain_uz": "Shoshilinchlik + qisqa havola + tahdid = klassik phishing uchligi.",
                    },
                    {
                        "q_en": "The domain 'paypa1-secure.xyz' is dangerous because…",
                        "q_uz": "'paypa1-secure.xyz' domeni xavfli, chunki…",
                        "opts_en": [
                            "It uses .xyz which is always evil",
                            "It contains a digit 1 instead of the letter L and extra words",
                            "It is too long",
                            "Domains with dashes don't exist",
                        ],
                        "opts_uz": [
                            ".xyz har doim yomon",
                            "L harfi o'rniga 1 raqami va ortiqcha so'zlar ishlatilgan",
                            "Juda uzun",
                            "Chiziqcha bilan domenlar mavjud emas",
                        ],
                        "correct": 1,
                        "explain_en": "Homograph tricks swap look-alike characters; always read the domain character by character.",
                        "explain_uz": "Homograf hiyla-nayranglari o'xshash belgilarni almashtiradi; domenlarni harfma-harf o'qing.",
                    },
                    {
                        "q_en": "What's the safest action when an email asks you to 'verify your password'?",
                        "q_uz": "Email 'parolni tasdiqlang' desa, eng xavfsiz harakat qaysi?",
                        "opts_en": [
                            "Reply with the password",
                            "Click the link quickly before it expires",
                            "Ignore the link; open the official site/app yourself",
                            "Forward it to friends to check",
                        ],
                        "opts_uz": [
                            "Parolni javobda yuborish",
                            "Havola muddati o'tishidan oldin tez bosish",
                            "Havolaga e'tibor bermaslik; rasmiy sayt/ilovani o'zingiz ochish",
                            "Tekshirish uchun do'stlarga yuborish",
                        ],
                        "correct": 2,
                        "explain_en": "Never authenticate through inbound links — navigate independently.",
                        "explain_uz": "Hech qachon tashqaridan kelgan havola orqali kirmang — o'zingiz mustaqil oching.",
                    },
                ],
            },
            {
                "id": "ph2",
                "title_en": "Social Media & Messenger Scams",
                "title_uz": "Ijtimoiy tarmoq va messdjer hiylalari",
                "body_en": (
                    "Scammers love messengers because people trust them. Three classics:\n\n"
                    "1️⃣ *The fake friend* — a cloned account of your friend asks to \"borrow money\" "
                    "or forwards a \"verification code\". Rule: *codes are NEVER forwarded*. A code "
                    "sent to you is a key to YOUR account.\n\n"
                    "2️⃣ *The fake job / crypto offer* — \"earn $500/day from home!\" They always "
                    "end the same way: you pay a 'fee' first, or your data is stolen.\n\n"
                    "3️⃣ *The QR / payment trick* — a stranger 'accidentally' sends money and asks "
                    "for a refund… from a different account. The original payment will be reversed "
                    "as stolen.\n\n"
                    "How to defend:\n"
                    "• Verify identity via a *voice or video call* on the old number\n"
                    "• Never share codes, passwords or card CVV — with *anyone*, even \"support\"\n"
                    "• Real companies never ask for payment via gift cards or personal transfers"
                ),
                "body_uz": (
                    "Hiylakorlar messdjerlarni yaxshi ko'radi, chunki odamlar ularga ishonadi. Uch "
                    "klassik sxema:\n\n"
                    "1️⃣ *Soxta do'st* — do'stingizning nusxalangan akkaunti \"pul qarz so'raydi\" "
                    "yoki \"tasdiqlash kodi\"ni yuborishni so'raydi. Qoida: *kodlar hech qachon "
                    "yuborilmaydi*. Sizga kelgan kod — SIZNING akkauntingiz kaliti.\n\n"
                    "2️⃣ *Soxta ish / kripto taklif* — \"uydan kuniga $500 ishlang!\" Oxiri doim "
                    "bir xil: avval 'to'lov' qilasiz yoki ma'lumotlaringiz o'girlanadi.\n\n"
                    "3️⃣ *QR / to'lov hiylasi* — begona odam 'tasodifan' pul yuboradi va boshqa "
                    "raqamga qaytarishni so'raydi. Asl to'lov o'g'irlangan deb qaytarib olinadi.\n\n"
                    "Himoya usullari:\n"
                    "• Shaxsni eski raqam orqali *ovozli yoki video qo'ng'iroq* bilan tasdiqlang\n"
                    "• Kodlar, parollar yoki karta CVVni *hech kimga*, hatto 'support'ga ham bermang\n"
                    "• Haqiqiy kompaniyalar hech qachon sovg'a kartalari yoki shaxsiy o'tkazmalar orqali to'lov so'ramaydi"
                ),
                "quiz": [
                    {
                        "q_en": "Your friend's account asks you to send them the code Telegram just sent you. What do you do?",
                        "q_uz": "Do'stingiz akkaunti Telegram yuborgan kodni unga yuborishni so'raydi. Nima qilasiz?",
                        "opts_en": [
                            "Send it quickly — it's your friend",
                            "Refuse and call your friend on their real number",
                            "Send only half of the code",
                            "Change your own password first",
                        ],
                        "opts_uz": [
                            "Tez yuboraman — bu mening do'stim",
                            "Rad etaman va do'stimning haqiqiy raqamiga qo'ng'iroq qilaman",
                            "Faqat kodning yarmisini yuboraman",
                            "Avval o'z parolimni o'zgartiraman",
                        ],
                        "correct": 1,
                        "explain_en": "The account is hijacked; the code would hand YOUR account to the attacker.",
                        "explain_uz": "Akkaunt o'zlashtirilgan; kod sizning akkauntingizni ham hujumchiga topshiradi.",
                    },
                    {
                        "q_en": "A stranger 'accidentally' sends you $200 and asks to return it to another card. This is…",
                        "q_uz": "Begona odam 'tasodifan' $200 yubordi va boshqa kartaga qaytarishni so'raydi. Bu…",
                        "opts_en": ["Just an honest mistake", "A reversal scam — don't send anything", "Free money", "A bank test"],
                        "opts_uz": ["Oddiy halol xato", "Qaytarib olish hiylasi — hech narsa yubormang", "Bepul pul", "Bank testi"],
                        "correct": 1,
                        "explain_en": "The original transfer will be reversed as stolen/fraudulent; the money you 'returned' is yours — lost.",
                        "explain_uz": "Asl to'lov o'g'irlangan deb qaytarib olinadi; siz 'qaytargan' pul esa sizniki — yo'qoladi.",
                    },
                    {
                        "q_en": "Which request is ALWAYS a scam sign?",
                        "q_uz": "Qaysi so'rov HAR DOIM hiyla belgisi?",
                        "opts_en": [
                            "Paying via gift cards or sharing a verification code",
                            "A newsletter subscription",
                            "Two-factor authentication setup",
                            "A password manager suggestion",
                        ],
                        "opts_uz": [
                            "Sovg'a kartalari orqali to'lash yoki kod ulashish",
                            "Yangiliklar obunasi",
                            "Ikki bosqichli tasdiqlashni sozlash",
                            "Parol menejeri tavsiyasi",
                        ],
                        "correct": 0,
                        "explain_en": "Legit organizations never need your codes, and gift cards are untraceable money.",
                        "explain_uz": "Haqiqiy tashkilotlar kodlaringizni so'ramaydi, sovg'a kartalari esa kuzatib bo'lmaydigan pul.",
                    },
                ],
            },
        ],
    },
    # ================================================================ module 3
    {
        "id": "mw",
        "icon": "🦠",
        "title_en": "Malware & Device Safety",
        "title_uz": "Zararli dasturlar va qurilma xavfsizligi",
        "lessons": [
            {
                "id": "mw1",
                "title_en": "Know Your Enemies: Malware Types",
                "title_uz": "Dushmanlaringizni taniing: zararli dastur turlari",
                "body_en": (
                    "*Malware* (malicious software) is any program designed to harm you. Know the "
                    "main species:\n\n"
                    "• *Virus / Worm* — spreads by infecting files or copying itself over networks\n"
                    "• *Trojan* — hides inside useful-looking software (a 'free game', a 'PDF reader')\n"
                    "• *Ransomware* — encrypts ALL your files and demands money for the key. Even "
                    "paying doesn't guarantee recovery!\n"
                    "• *Spyware / Keylogger* — silently records everything: passwords, messages, "
                    "bank logins\n"
                    "• *Adware* — floods you with ads and tracks your behavior\n\n"
                    "Defense basics:\n"
                    "1. Update your OS and apps — updates patch the holes malware crawls through\n"
                    "2. Install software only from *official stores*\n"
                    "3. Keep backups (3-2-1 rule: 3 copies, 2 media, 1 offsite) — ransomware's only real cure\n"
                    "4. Don't plug unknown USB drives into your computer"
                ),
                "body_uz": (
                    "*Zararli dastur* (malware) — sizga zarar yetkazish uchun yaratilgan har qanday "
                    "dastur. Asosiy turlarini taniylik:\n\n"
                    "• *Virus / Qurt (Worm)* — fayllarni yuqtirish yoki tarmoq bo'ylab ko'chib tarqaladi\n"
                    "• *Trojan* — foydali ko'rinishgan dastur ichida yashiringan ('bepul o'yin', 'PDF o'quvchi')\n"
                    "• *Ransomware* — barcha fayllaringizni shifrlaydi va kalit uchun pul talab qiladi. "
                    "To'lash ham tiklash kafolatlamaydi!\n"
                    "• *Shpion dastur (Spyware / Keylogger)* — jimjillik hammasini yozib oladi: parollar, "
                    "xabarlar, bank ma'lumotlari\n"
                    "• *Reklama dasturi (Adware)* — reklama bilan to'sib qo'yadi va xatti-harakatlaringizni kuzatadi\n\n"
                    "Himoya asoslari:\n"
                    "1. OS va ilovalarni yangilab turing — yangilanishlar zararli dastur kiradigan teshiklarni yamaydi\n"
                    "2. Dasturlarni faqat *rasmiy do'konlardan* o'rnating\n"
                    "3. Zaxira nusxalar saqlang (3-2-1 qoidasi: 3 nusxa, 2 xil vosita, 1 tashqarida) — ransomware'ning yagona haqiqiy davosi\n"
                    "4. Notanish USB fleshkalarni kompyuterga ulamang"
                ),
                "quiz": [
                    {
                        "q_en": "Which malware encrypts your files and demands payment?",
                        "q_uz": "Qaysi zararli dastur fayllarni shifrlab pul talab qiladi?",
                        "opts_en": ["Adware", "Ransomware", "Keylogger", "Worm"],
                        "opts_uz": ["Adware", "Ransomware", "Keylogger", "Qurt (Worm)"],
                        "correct": 1,
                        "explain_en": "Ransom = money demanded; it holds your data hostage.",
                        "explain_uz": "Ransom = talab qilingan pul; u ma'lumotlaringizni garovda ushlab turadi.",
                    },
                    {
                        "q_en": "What is the 3-2-1 backup rule?",
                        "q_uz": "3-2-1 zaxira qoidasi nima?",
                        "opts_en": [
                            "3 passwords, 2 emails, 1 phone",
                            "3 copies, 2 different media, 1 stored offsite",
                            "3 updates per month, 2 scans, 1 antivirus",
                            "3 firewalls, 2 VPNs, 1 proxy",
                        ],
                        "opts_uz": [
                            "3 parol, 2 email, 1 telefon",
                            "3 nusxa, 2 xil vosita, 1 tashqarida saqlangan",
                            "Oyda 3 yangilanish, 2 tekshiruv, 1 antivirus",
                            "3 faol ravish, 2 VPN, 1 proksi",
                        ],
                        "correct": 1,
                        "explain_en": "With an offline/offsite copy, ransomware can't lock you out of everything.",
                        "explain_uz": "Oflayn/tashqaridagi nusxa bo'lsa, ransomware sizni butunlay bloklolmaydi.",
                    },
                    {
                        "q_en": "Why are software updates important for security?",
                        "q_uz": "Dastur yangilanishlari xavfsizlik uchun nega muhim?",
                        "opts_en": [
                            "They add new emojis",
                            "They patch security holes that malware exploits",
                            "They make the computer faster only",
                            "They are not important at all",
                        ],
                        "opts_uz": [
                            "Yangi emojilar qo'shadi",
                            "Zararli dasturlar foydalanadigan xavfsizlik teshiklarini yamaydi",
                            "Faqat kompyuterni tezlashtiradi",
                            "Umuman muhim emas",
                        ],
                        "correct": 1,
                        "explain_en": "Most successful attacks use known, already-patched vulnerabilities.",
                        "explain_uz": "Ko'pgina muvaffaqiyatli hujumlar ma'lum, allaqachon yamalgan zaifliklardan foydalanadi.",
                    },
                ],
            },
            {
                "id": "mw2",
                "title_en": "Public Wi-Fi, VPNs & Safe Browsing",
                "title_uz": "Ommaviy Wi-Fi, VPN va xavfsiz brauzer",
                "body_en": (
                    "Free airport or café Wi-Fi is convenient — and dangerous. On an open network, "
                    "an attacker can run a *man-in-the-middle* attack or create an *evil twin* — a "
                    "fake hotspot named 'Airport_Free_WiFi' that records your traffic.\n\n"
                    "Safe habits:\n"
                    "• Prefer *mobile data* for banking and logins\n"
                    "• On public Wi-Fi use a *VPN* — it encrypts your traffic so snoopers see only noise\n"
                    "• Check for *HTTPS* and the padlock 🔒 — but remember: a padlock means "
                    "'encrypted', NOT 'safe'! Phishing sites have HTTPS too\n"
                    "• Disable *auto-connect* to open networks\n"
                    "• Turn off file sharing when on public networks\n\n"
                    "Bonus — browser hygiene: use an ad/tracker blocker, review browser extensions "
                    "(each one can read your pages!), and sign out of sensitive accounts on shared devices."
                ),
                "body_uz": (
                    "Aeroport yoki kafedagi bepul Wi-Fi qulay — va xavfli. Ochiq tarmoqda hujumchi "
                    "*man-in-the-middle* hujumini qilishi yoki *evil twin* — trafikingizni yozib "
                    "oluvchi soxta *Airport_Free_WiFi* nuqtasini yaratishi mumkin.\n\n"
                    "Xavfsiz odatlar:\n"
                    "• Banking va kirish uchun *mobil internetni* afzal ko'ring\n"
                    "• Ommaviy Wi-Fi'da *VPN* ishlating — u trafikingizni shifrlaydi, josuslar faqat shovqin ko'radi\n"
                    "• *HTTPS* va qulf 🔒 belgisini tekshiring — lekin esda tutang: qulf 'shifrlangan' "
                    "degani, 'xavfsiz' degani EMAS! Phishing saytlarida ham HTTPS bor\n"
                    "• Ochiq tarmoqlarga *avtomatik ulanishni* o'chirib qo'ying\n"
                    "• Ommaviy tarmoqda fayl almashishni o'chiring\n\n"
                    "Bonus — brauzer gigienasi: reklama/kuzatuv blokatoridan foydalaning, brauzer "
                    "kengaytmalarini tekshiring (har biri sahifalaringizni o'qiy oladi!), umumiy "
                    "qurilmalarda maxfiy akkauntlardan chiqib qo'ying."
                ),
                "quiz": [
                    {
                        "q_en": "What is an 'evil twin' hotspot?",
                        "q_uz": "'Evil twin' nuqtasi nima?",
                        "opts_en": [
                            "A hotspot that shares your connection with others",
                            "A fake Wi-Fi access point that imitates a legitimate one",
                            "A Wi-Fi network with two passwords",
                            "A premium double-speed network",
                        ],
                        "opts_uz": [
                            "Ulanishni boshqalar bilan bo'lishuvchi nuqta",
                            "Haqiqiy nuqtani taqlid qiluvchi soxta Wi-Fi nuqtasi",
                            "Ikki parolli Wi-Fi tarmoq",
                            "Ikki barobar tez premium tarmoq",
                        ],
                        "correct": 1,
                        "explain_en": "Attackers clone a network name to intercept everything you send.",
                        "explain_uz": "Hujumchilar tarmoq nomini nusxalab, yuborgan hamma narsangizni ushlaydi.",
                    },
                    {
                        "q_en": "A website shows the padlock 🔒. What does this guarantee?",
                        "q_uz": "Saytda qulf 🔒 bor. Bu nimani kafolatlaydi?",
                        "opts_en": [
                            "The site is safe and honest",
                            "The connection is encrypted — nothing more",
                            "The site is government-approved",
                            "There are no ads on the site",
                        ],
                        "opts_uz": [
                            "Sayt xavfsiz va halol",
                            "Ulanish shifrlangan — boshqa hech narsa",
                            "Sayt davlat tomonidan tasdiqlangan",
                            "Saytda reklama yo'q",
                        ],
                        "correct": 1,
                        "explain_en": "HTTPS encrypts traffic; it says nothing about the site's intentions.",
                        "explain_uz": "HTTPS trafikni shifrlaydi; sayt niyatlari haqida hech narsa aytmaydi.",
                    },
                    {
                        "q_en": "Best practice for online banking on the road?",
                        "q_uz": "Yo'lda onlayn banking qilishning eng yaxshi usuli?",
                        "opts_en": [
                            "Use open café Wi-Fi without VPN",
                            "Use mobile data or a trusted VPN",
                            "Ask a stranger for their hotspot",
                            "Connect to any network named 'Free'",
                        ],
                        "opts_uz": [
                            "VPNsiz ochiq kafe Wi-Fi'ini ishlatish",
                            "Mobil internet yoki ishonchli VPN ishlatish",
                            "Begonadan uning hotspotini so'rash",
                            "'Free' deb nomlangan har qanday tarmoqqa ulanish",
                        ],
                        "correct": 1,
                        "explain_en": "Mobile data is far harder to intercept than shared public Wi-Fi.",
                        "explain_uz": "Mobil internetni umumiy Wi-Fi'ga qaraganda ushlash ancha qiyin.",
                    },
                ],
            },
        ],
    },
]


# ------------------------------------------------------------------ helpers --

def all_lessons() -> list[dict]:
    """Flat list of all lessons, each with a 'module' reference."""
    out = []
    for mod in MODULES:
        for les in mod["lessons"]:
            out.append({**les, "module": {k: mod[k] for k in ("id", "icon", "title_en", "title_uz")}})
    return out


def get_lesson(lesson_id: str) -> dict | None:
    for les in all_lessons():
        if les["id"] == lesson_id:
            return les
    return None


def get_module_by_lesson(lesson_id: str) -> dict | None:
    for mod in MODULES:
        if any(l["id"] == lesson_id for l in mod["lessons"]):
            return mod
    return None


def next_lesson(lesson_id: str) -> dict | None:
    lessons = all_lessons()
    for i, les in enumerate(lessons):
        if les["id"] == lesson_id and i + 1 < len(lessons):
            return lessons[i + 1]
    return None


TOTAL_LESSONS = len(all_lessons())
