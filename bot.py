import telebot
import json
import requests
import random
import time
import re
import threading
from datetime import datetime
from faker import Faker

# ==============================================================================
# إعدادات البوت الأساسية
# ==============================================================================

TOKEN = "8719808324:AAFt-vGpbiy9uEku2xSTJ7SbJbLg9QvfpnU"
bot = telebot.TeleBot(TOKEN)

# اذكر المصدر @Abosgr2025 • https://t.me/+YNZRwbLWXRZjMmVk
# • BLACK LEGO 👋

# ==============================================================================
# الإيموجيات المتحركة Premium (لتحسين واجهة المستخدم)
# ==============================================================================
EMOJI_CROWN = "5017184459347199280"         # 1
EMOJI_DIAMOND = "5017181010488460393"       # 2
EMOJI_STAR = "5017218054581388213"          # 3
EMOJI_SPARKLES = "5019656878745978138"      # 4
EMOJI_FIRE = "5019401809228202926"          # 5
EMOJI_GEM = "5019759644428469277"           # 6
EMOJI_ROCKET = "5017341470466639017"        # 7
EMOJI_SHIELD = "5019584761950110887"        # 8
EMOJI_KEY = "5019569849823659365"           # 9
EMOJI_MAIL = "5019765756166931507"          # 10
EMOJI_USER = "5017191095071671290"          # 11
EMOJI_SUCCESS = "5019651033295487811"       # 12
EMOJI_FAIL = "5017073954133640188"          # 13
EMOJI_GLOBE = "5017154574964753399"         # 14
EMOJI_LOCK = "5019373307825226748"          # 15
EMOJI_TIME = "5017497085721708142"          # 16
EMOJI_STATS = "5017098860648989669"         # 17
EMOJI_HEART = "5017351305941746807"         # 18
EMOJI_SETTINGS = "5017558392084890552"      # 19
EMOJI_LOADING = "5019348457144452062"       # 20

# ==============================================================================
# بيانات المستخدمين والإحصائيات
# ==============================================================================
user_data = {}
global_stats = {"created": 0, "failed": 0}

# ==============================================================================
# دوال إدارة الحسابات (قاعدة بيانات بسيطة بملف JSON)
# ==============================================================================
def save_account_to_db(user_id, account_info):
    """يحفظ معلومات الحساب في ملف JSON خاص بالمستخدم."""
    try:
        with open("accounts_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}
    
    uid = str(user_id)
    if uid not in db:
        db[uid] = []
    
    db[uid].append(account_info)
    
    with open("accounts_db.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

def get_user_accounts(user_id):
    """يسترجع قائمة الحسابات المحفوظة للمستخدم."""
    try:
        with open("accounts_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
            return db.get(str(user_id), [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ==============================================================================
# دوال فيسبوك (لإنشاء الحسابات وفحصها وجلب البيانات)
# ==============================================================================
def get_regex_group(pattern, text, default_value=""):
    """يستخرج مجموعة من النص باستخدام التعبيرات العادية."""
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return default_value

def get_fake_desktop_ua():
    """يولد وكيل مستخدم (User-Agent) عشوائي لمحاكاة متصفح سطح المكتب."""
    desktop_uas = [
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "width": 1920,
            "browser": "Microsoft Edge",
            "version": "138",
            "full_version_list": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Microsoft Edge";v="138.0.3351.121"'
        },
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) "
                  "Gecko/20100101 Firefox/119.0",
            "width": 1920,
            "browser": "Firefox",
            "version": "119",
            "full_version_list": '"Firefox";v="119.0"'
        },
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36",
            "width": 1920,
            "browser": "Chromium",
            "version": "138",
            "full_version_list": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184"'
        }
    ]
    return random.choice(desktop_uas)

def parse_set_cookie(headers):
    """يحلل رأس 'Set-Cookie' ويستخرج الكوكيز."""
    raw_cookie = headers.get('Set-Cookie')
    cookies = {}
    if not raw_cookie:
        return cookies, ""
    parts = raw_cookie.split(',')
    temp = []
    for part in parts:
        if '=' in part.split(';')[0]:
            temp.append(part.strip())
        else:
            temp[-1] += ',' + part.strip()
    for ck in temp:
        kv = ck.split(';', 1)[0]
        if '=' in kv:
            k, v = kv.split('=', 1)
            cookies[k.strip()] = v.strip()
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    return cookies, cookie_str

def create_facebook_account(password=None):
    """ينشئ حساب فيسبوك جديد بشكل تلقائي."""
    fake = Faker('en_US')
    ua_data = get_fake_desktop_ua()
    first_name = fake.first_name_female()
    last_name = fake.last_name()
    email_akun = f'{first_name.lower()}{last_name.lower()}{random.randint(10,99)}@gmail.com'
    if password is None:
        password = 'levi@$618pi'

    cookies = {'wd': '738x688', 'locale': 'en_GB'}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,id;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': f'"Not)A;Brand";v="8", "{ua_data["browser"]}";v="{ua_data["version"]}"',
        'sec-ch-ua-full-version-list': ua_data["full_version_list"],
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua_data["ua"],
        'viewport-width': str(ua_data["width"])
    }

    try:
        response = requests.get(
            'https://www.facebook.com/?_rdc=1&_rdr',
            cookies=cookies,
            headers=headers,
            timeout=30
        )
        cookies.update(dict(response.cookies.get_dict()))
        headers.update({'referer': 'https://www.facebook.com/?_rdc=1&_rdr'})
        
        signup = requests.get(
            'https://www.facebook.com/r.php?entry_point=login',
            cookies=cookies,
            headers=headers,
            timeout=30
        ).text.replace('\\', '')
        
        lsd_token = 'AVo86L310qI'
        haste_session = get_regex_group('"haste_session":"(.*?)"', signup)
        ccg = get_regex_group('"connectionClass":"(.*?)"', signup)
        rev = get_regex_group(r'"consistency":{"rev":(\d+)', signup)
        hsi = get_regex_group(r'"hsi":"(\d+)"', signup)
        spint = get_regex_group(r'"__spin_t":(\d+)', signup)
        vip = get_regex_group('"vip":"(.*?)"', signup)
        
        headers.update({
            'x-asbd-id': '359341',
            'x-fb-lsd': lsd_token
        })

        requests.get(
            f'https://web.facebook.com/ajax/registration/validation/contactpoint_invalid/?contactpoint={email_akun}&fb_dtsg_ag&__user=0&__a=1&__req=4&__hs={haste_session}&dpr=1&__ccg={ccg}&__rev={rev}&__s=an0im4%3Afuzmdi%3Ahsr1au&__hsi={hsi}&__dyn=7xe6EsK36Q5E5ObwKBWg5S1Dxu13wqovzEdEc8uw9-3K0lW4o3Bw5VCwjE3awdu0FE2awpUO0n24o5-0me1Fw5uwbO0KU3mwaS0zE5W09yyE1582ZwrU1Xo1UU3jwea&__hsdp=hIfEA5EIox0IkE99fxTFBAwNy2wJBCx90NhE4a1nxe0ky0mK0MEMw7W1kwk87Feoqh0&__hblp=0PU2Owjo620kq0k63a0tG1ew9W2a0cZAw3q80zS0-o04XK0Go1pU0OG1uKLDBFoDh80rQw&__spin_r={rev}&__spin_b=trunk&__spin_t={spint}',
            cookies=cookies,
            headers=headers,
            timeout=30
        )

        headers.update({
            'origin': 'https://www.facebook.com',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Microsoft Edge";v="138.0.3351.121"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'accept': '*/*',
            'accept-language': 'en,id;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://www.facebook.com/r.php?entry_point=login',
            'cookie': 'datr=gKGYaMFDH3Zw5Gg2sggX9tbi; sb=gKGYaLge53jtbcJoymqEnZXl; ps_l=1; ps_n=1; locale=en_GB; wd=738x688; fr=1HLHrBbAGkoJv5O1l.AWeSwdELticByfVx58z4uY-kWUf_iGff96qe3DzSwDRT0GEF8Jo.BomL39..AAA.0.0.BomL4I.AWddslGP88dg7QDodcwbRuVHL_k'
        })

        data = {
            'jazoest': get_regex_group(r'name="jazoest" value="(\d+)"', signup),
            'lsd': lsd_token,
            'firstname': first_name,
            'lastname': last_name,
            'birthday_day': '10',
            'birthday_month': '8',
            'birthday_year': '2005',
            'birthday_age': '',
            'did_use_age': 'false',
            'sex': '1',
            'preferred_pronoun': '',
            'custom_gender': '',
            'reg_email__': email_akun,
            'reg_email_confirmation__': '',
            'reg_passwd__': f'#PWD_BROWSER:0:{int(time.time())}:{password}',
            'referrer': '',
            'asked_to_login': '0',
            'use_custom_gender': '',
            'terms': 'on',
            'ns': '0',
            'ri': get_regex_group('name="ri" value="(.?)"', signup),
            'action_dialog_shown': '',
            'invid': '',
            'a': '',
            'oi': '',
            'locale': 'en_GB',
            'app_bundle': '',
            'app_data': '',
            'reg_data': '',
            'app_id': '',
            'fbpage_id': '',
            'reg_oid': '',
            'reg_instance': get_regex_group('name="reg_instance" value="(.?)"', signup),
            'openid_token': '',
            'uo_ip': vip,
            'guid': '',
            'key': '',
            're': '',
            'mid': '',
            'fid': '',
            'reg_dropoff_id': '',
            'reg_dropoff_code': '',
            'ignore': 'captcha|reg_email_confirmation__',
            'captcha_persist_data': get_regex_group('name="captcha_persist_data" value="(.*?)"', signup),
            'captcha_response': '',
            '__user': '0',
            '__a': '1',
            '__req': '5',
            '__hs': haste_session,
            'dpr': '1',
            '__ccg': ccg,
            '__rev': rev,
            '__s': 'an0im4:fuzmdi:hsr1su',
            '__hsi': hsi,
            '__dyn': '7xe6EsK36Q5E5ObwKBWg5S1Dxu13wqovzEdEc8uw9-3K0lW4o3Bw5VCwjE3awdu0FE2awpUO0n24o5-0me1Fw5uwbO0KU3mwaS0zE5W09yyE1582ZwrU1Xo1UU3jwea',
            '__hsdp': 'hIfEA5EIox0IkE99fxTFBAwNy2wJBCx90NhE4a1nxe0ky0mK0MEMw7W1kwk87Feoqh0',
            '__hblp': '0PU2Owjo620kq0k63a0tG1ew9W2a0cZAw3q80zS0-o04XK0Go1pU0OG1uKLDBFoDh80rQw',
            '__spin_r': rev,
            '__spin_b': 'trunk',
            '__spin_t': spint
        }

        response = requests.post(
            'https://web.facebook.com/ajax/register.php',
            headers=headers,
            data=data,
            timeout=30
        )

        if '"registration_succeeded":true' in response.text:
            cookie_dict, cookie_str = parse_set_cookie(response.headers)
            return {
                "success": True,
                "first_name": first_name,
                "last_name": last_name,
                "email": email_akun,
                "password": password,
                "cookie": cookie_str,
                "ip": vip
            }
        else:
            error_msg = "Unknown error"
            if "error" in response.text.lower():
                try:
                    error_data = response.json()
                    error_msg = str(error_data.get("error", "Unknown error"))[:200]
                except:
                    error_msg = response.text[:200]
            return {"success": False, "error": error_msg}
    except Exception as e:
        return {"success": False, "error": str(e)[:200]}

def get_facebook_headers(cookies_str):
    """يجهز رؤوس الطلب (Headers) لطلبات فيسبوك."""
    return {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookies_str,
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.188"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

def check_account_status(cookies_str):
    """يفحص حالة حساب فيسبوك باستخدام الكوكيز."""
    headers = get_facebook_headers(cookies_str)
    try:
        response = requests.get('https://www.facebook.com/profile.php', headers=headers, timeout=15)
        if 'checkpoint' in response.url or 'login.php' in response.url:
            return {"status": "banned/locked", "message": "الحساب محظور أو يتطلب تسجيل دخول (Checkpoint)"}
        if 'c_user' in cookies_str:
            return {"status": "active", "message": "الحساب نشط ويعمل بشكل جيد"}
        return {"status": "unknown", "message": "لم يتم التعرف على حالة الحساب"}
    except Exception as e:
        return {"status": "error", "message": f"خطأ أثناء الفحص: {str(e)}"}

def fetch_account_data(cookies_str):
    """يجلب الاسم الحقيقي وعدد الأصدقاء وحالة الحساب من فيسبوك."""
    headers = get_facebook_headers(cookies_str)
    try:
        response = requests.get('https://www.facebook.com/me', headers=headers, timeout=15)
        text = response.text
        
        # جلب الاسم الحقيقي
        name_match = re.search(r'<title>(.*?)</title>', text)
        real_name = name_match.group(1).split('|')[0].strip() if name_match else "غير معروف"
        if "Facebook" in real_name or not real_name:
            real_name = "مستخدم فيسبوك"

        # جلب عدد الأصدقاء (محاولة أولية)
        friends_match = re.search(r'(\d+)\s+friends', text)
        friend_count = friends_match.group(1) if friends_match else "0"

        return {
            "success": True,
            "real_name": real_name,
            "friend_count": friend_count,
            "status": "نشط",
            "message": "تم جلب البيانات بنجاح"
        }
    except Exception as e:
        return {"success": False, "message": f"خطأ أثناء جلب البيانات: {str(e)}"}

def perform_automated_task(cookies_str, task_type):
    """ينفذ مهام تلقائية على حساب فيسبوك (قيد التطوير)."""
    headers = get_facebook_headers(cookies_str)
    try:
        # هذه الوظائف تتطلب FB_DTSG و JAZOEST للقيام بعمليات النشر
        # محاولة جلب التوكنات اللازمة
        res = requests.get('https://www.facebook.com/', headers=headers, timeout=15)
        fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
        jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
        
        if task_type == "post_welcome":
            # مثال بسيط لمنشور ترحيبي (يتطلب معرفة الـ User ID و endpoint محددة)
            return {"success": False, "message": "وظيفة النشر التلقائي تتطلب إعدادات إضافية للـ API"}
        
        return {"success": False, "message": "المهمة غير متوفرة حالياً"}
    except Exception as e:
        return {"success": False, "message": f"خطأ في المهمة: {str(e)}"}

# ==============================================================================
# دوال مساعدة لواجهة المستخدم (الرسوم المتحركة)
# ==============================================================================
def show_loading_animation(chat_id, msg_id, stop_event):
    """يعرض رسوم متحركة للتحميل في رسالة تيليجرام."""
    frames = ["▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰"]
    i = 0
    
    while not stop_event.is_set():
        frame = frames[i % len(frames)]
        
        text = (
            f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري المعالجة...</b>\n'
            f'<blockquote>[{frame}]</blockquote>'
        )
        
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                parse_mode='HTML'
            )
        except:
            pass
        
        i += 1
        time.sleep(0.8)

# ==============================================================================
# أوامر البوت ومعالجة الاستدعاءات (Handlers)
# ==============================================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """يرسل رسالة الترحيب مع الأزرار الرئيسية."""
    welcome_text = (
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji> <b>FACEBOOK GEN</b>\n'
        f'<blockquote>أداة إنشاء حسابات فيسبوك تلقائياً</blockquote>\n\n'
        f'<blockquote expandable>\n'
        f'<b>⎔ المطور:</b> <a href="https://t.me/Abosgr2024">𝔸𝔹𝕆𝕊𝔾ℝ 𝕐𝔼𝕄𝔼ℕ</a>\n'
        f'</blockquote>'
    )

    keyboard = [
        # الصف الأول: زر أساسي ومهم (زر بحجم كامل)
        [
            {
                "text": "إنشاء حساب",
                "callback_data": "create_single",
                "style": "success",
                "icon_custom_emoji_id": EMOJI_ROCKET
            }
        ],
        # الصف الثاني: خيارات إضافية (زرين بجانب بعض لتوفير المساحة وتجميل الشكل)
        [
            {
                "text": "إنشاء بالجملة",
                "callback_data": "menu_bulk",
                "style": "primary",
                "icon_custom_emoji_id": EMOJI_FIRE
            },
            {
                "text": "تغيير الباسورد",
                "callback_data": "change_password",
                "style": "primary",
                "icon_custom_emoji_id": EMOJI_KEY
            }
        ],
        # الصف الثالث: زر المعلومات (زر بحجم كامل في الأسفل)
        [
            {
                "text": "عن المطور",
                "callback_data": "about_dev",
                "style": "primary",
                "icon_custom_emoji_id": EMOJI_DIAMOND
            }
        ],
        [
            {
                "text": "مدير الحسابات",
                "callback_data": "account_manager_menu",
                "style": "info",
                "icon_custom_emoji_id": EMOJI_USER
            }
        ]
    ]

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML',
        reply_markup=json.dumps({"inline_keyboard": keyboard}),
        disable_web_page_preview=True
    )


def show_account_result(chat_id, msg_id, result):
    """يعرض نتيجة إنشاء حساب واحد."""
    if result["success"]:
        global_stats["created"] += 1
        
        success_text = (
            f'<tg-emoji emoji-id="{EMOJI_SUCCESS}">✅</tg-emoji> <b>تم الإنشاء بنجاح</b>\n'
            f'<blockquote expandable>\n'
            f'<b>👤 الاسم:</b> <code>{result["first_name"]} {result["last_name"]}</code>\n'
            f'<b>📧 الإيميل:</b> <code>{result["email"]}</code>\n'
            f'<b>🔒 الباسورد:</b> <code>{result["password"]}</code>\n'
            f'<b>🌐 IP:</b> <code>{result["ip"]}</code>\n\n'
            f'<b>🍪 الكوكيز:</b>\n<code>{result["cookie"]}</code>\n'
            f'</blockquote>'
        )
        
        # open('akun_id', 'a').write(f'{result["cookie"]}|{result["password"]}\n') # تم التعليق عليه لأنه تم استبداله بـ save_account_to_db
        
        keyboard = [
            [
                {
                    "text": "إنشاء آخر",
                    "callback_data": "create_another",
                    "style": "success",
                    "icon_custom_emoji_id": EMOJI_ROCKET
                },
                {
                    "text": "رجوع",
                    "callback_data": "back_to_start",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_SHIELD
                }
            ]
        ]
    
    else:
        global_stats["failed"] += 1
        
        success_text = (
            f'<tg-emoji emoji-id="{EMOJI_FAIL}">❌</tg-emoji> <b>فشل الإنشاء</b>\n'
            f'<blockquote expandable>{result["error"][:150]}</blockquote>'
        )
        
        keyboard = [
            [
                {
                    "text": "محاولة أخرى",
                    "callback_data": "create_another",
                    "style": "success",
                    "icon_custom_emoji_id": EMOJI_ROCKET
                },
                {
                    "text": "رجوع",
                    "callback_data": "back_to_start",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_SHIELD
                }
            ]
        ]
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=success_text,
        parse_mode='HTML',
        reply_markup=json.dumps({"inline_keyboard": keyboard})
    )

def process_bulk_accounts(chat_id, user_id, count):
    """ينشئ مجموعة من الحسابات ويرسل كل حساب برسالة منفصلة فور إنشائه."""
    loading_msg = bot.send_message(
        chat_id,
        f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>تجهيز {count} حساب...</b>',
        parse_mode='HTML'
    )
    
    password = user_data[user_id].get("password", "levi@$618pi")
    success_list = []
    fail_count = 0
    
    for i in range(1, count + 1):
        progress = int(i / count * 100)
        bar = "▰" * (progress // 10) + "▱" * (10 - progress // 10)
        
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=loading_msg.message_id,
                text=(
                    f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji> <b>إنشاء {count} حساب</b>\n'
                    f'<blockquote expandable>\n'
                    f'<b>التقدم:</b> {i}/{count}\n'
                    f'<b>الشريط:</b> [{bar}] {progress}%\n'
                    f'<b>ناجح:</b> {len(success_list)} | <b>فاشل:</b> {fail_count}\n'
                    f'</blockquote>'
                ),
                parse_mode='HTML'
            )
        except:
            pass
        
        result = create_facebook_account(password)
        
        if result["success"]:
            success_list.append(result)
            global_stats["created"] += 1
            
            # إرسال الحساب في رسالة منفصلة بصندوق مطوي فور إنشائه
            acc_text = (
                f'<tg-emoji emoji-id="{EMOJI_SUCCESS}">✅</tg-emoji> <b>تم إنشاء حساب بنجاح ({len(success_list)})</b>\n'
                f'<blockquote expandable>\n'
                f'<b>👤 الاسم:</b> <code>{result["first_name"]} {result["last_name"]}</code>\n'
                f'<b>📧 الإيميل:</b> <code>{result["email"]}</code>\n'
                f'<b>🔒 الباسورد:</b> <code>{result["password"]}</code>\n'
                f'<b>🌐 IP:</b> <code>{result["ip"]}</code>\n\n'
                f'<b>🍪 الكوكيز:</b>\n<code>{result["cookie"]}</code>\n'
                f'</blockquote>'
            )
            bot.send_message(chat_id, acc_text, parse_mode='HTML')
            save_account_to_db(user_id, result)
            
        else:
            fail_count += 1
            global_stats["failed"] += 1
        
        if i < count:
            time.sleep(random.randint(5, 10))
    
    # حذف رسالة التحميل المستمرة
    try:
        bot.delete_message(chat_id, loading_msg.message_id)
    except:
        pass
    
    now = datetime.now()
    
    # رسالة الملخص النهائي مع الأزرار
    final_text = (
        f'<tg-emoji emoji-id="{EMOJI_SUCCESS}">✅</tg-emoji> <b>اكتمل الإنشاء بالجملة!</b>\n'
        f'<blockquote expandable>\n'
        f'✅ <b>ناجح:</b> {len(success_list)}\n'
        f'❌ <b>فاشل:</b> {fail_count}\n'
        f'⏱️ <b>{now.strftime("%H:%M:%S")}</b>\n'
        f'</blockquote>'
    )
    
    keyboard = [
        [
            {
                "text": "إنشاء آخر",
                "callback_data": "create_another",
                "style": "success",
                "icon_custom_emoji_id": EMOJI_ROCKET
            }
        ],
        [
            {
                "text": "رجوع",
                "callback_data": "back_to_start",
                "style": "danger",
                "icon_custom_emoji_id": EMOJI_SHIELD
            }
        ]
    ]
    
    bot.send_message(
        chat_id,
        final_text,
        parse_mode='HTML',
        reply_markup=json.dumps({"inline_keyboard": keyboard})
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """يعالج جميع استدعاءات الأزرار المضمنة (Inline Keyboard Buttons)."""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if user_id not in user_data:
        user_data[user_id] = {"password": "levi@$618pi", "state": "idle"}
    
    # حذف الرسالة
    if call.data == "delete_msg":
        try:
            bot.delete_message(chat_id, msg_id)
        except:
            pass
        return
    
    # قائمة مدير الحسابات
    elif call.data == "account_manager_menu":
        accounts = get_user_accounts(user_id)
        if not accounts:
            manager_text = (
                f'<tg-emoji emoji-id="{EMOJI_USER}">👤</tg-emoji> <b>مدير الحسابات</b>\n'
                f'<blockquote>لا يوجد حسابات منشأة حالياً. قم بإنشاء حساب أولاً.</blockquote>'
            )
            manager_keyboard = [[{"text": "رجوع", "callback_data": "back_to_start", "style": "danger", "icon_custom_emoji_id": EMOJI_SHIELD}]]
        else:
            manager_text = (
                f'<tg-emoji emoji-id="{EMOJI_USER}">👤</tg-emoji> <b>مدير الحسابات</b>\n'
                f'<blockquote>اختر الحساب الذي تريد إدارته:</blockquote>'
            )
            manager_keyboard = []
            for idx, acc in enumerate(accounts):
                manager_keyboard.append([{
                    "text": f"👤 {acc['first_name']} {acc['last_name']}",
                    "callback_data": f"manage_acc_{idx}"
                }])
            manager_keyboard.append([{"text": "رجوع", "callback_data": "back_to_start", "style": "danger", "icon_custom_emoji_id": EMOJI_SHIELD}])

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=manager_text,
            parse_mode='HTML',
            reply_markup=json.dumps({"inline_keyboard": manager_keyboard})
        )

    # إدارة حساب محدد
    elif call.data.startswith("manage_acc_"):
        acc_idx = int(call.data.split("_")[-1])
        accounts = get_user_accounts(user_id)
        if acc_idx < len(accounts):
            acc = accounts[acc_idx]
            user_data[user_id]["selected_acc"] = acc
            
            manage_text = (
                f'<tg-emoji emoji-id="{EMOJI_USER}">👤</tg-emoji> <b>إدارة الحساب:</b> {acc["first_name"]} {acc["last_name"]}\n'
                f'<blockquote>اختر الإجراء المطلوب:</blockquote>'
            )
            manage_keyboard = [
                [
                    {"text": "فحص الحالة", "callback_data": "action_check_status", "style": "primary", "icon_custom_emoji_id": EMOJI_GLOBE},
                    {"text": "جلب البيانات", "callback_data": "action_fetch_data", "style": "primary", "icon_custom_emoji_id": EMOJI_STATS}
                ],
                [{"text": "مهام تلقائية", "callback_data": "action_auto_tasks", "style": "primary", "icon_custom_emoji_id": EMOJI_SETTINGS}],
                [{"text": "رجوع للقائمة", "callback_data": "account_manager_menu", "style": "danger", "icon_custom_emoji_id": EMOJI_SHIELD}]
            ]
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=manage_text, parse_mode='HTML', reply_markup=json.dumps({"inline_keyboard": manage_keyboard}))

    # تنفيذ الإجراءات على الحساب المختار
    elif call.data.startswith("action_"):
        action = call.data.replace("action_", "")
        acc = user_data[user_id].get("selected_acc")
        if not acc:
            bot.answer_callback_query(call.id, "لم يتم اختيار حساب!", show_alert=True)
            return

        cookies = acc.get("cookie", "")
        
        loading_msg = bot.send_message(chat_id, f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري المعالجة...</b>', parse_mode='HTML')
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=show_loading_animation, args=(chat_id, loading_msg.message_id, stop_event))
        anim_thread.start()

        if action == "check_status":
            res = check_account_status(cookies)
            text = f'<tg-emoji emoji-id="{EMOJI_SUCCESS if res["status"] == "active" else EMOJI_FAIL}">{res["status"]}</tg-emoji> <b>النتيجة:</b> {res["message"]}'
        elif action == "fetch_data":
            res = fetch_account_data(cookies)
            if res["success"]:
                text = (f'<b>👤 الاسم:</b> <code>{res["real_name"]}</code>\n'
                        f'<b>👥 الأصدقاء:</b> <code>{res["friend_count"]}</code>\n'
                        f'<b>🟢 الحالة:</b> <code>{res["status"]}</code>')
            else:
                text = f'❌ <b>فشل:</b> {res["message"]}'
        elif action == "auto_tasks":
            text = "⚙️ <b>المهام التلقائية قيد التطوير...</b>"
        
        stop_event.set()
        anim_thread.join(timeout=1)
        
        keyboard = [[{"text": "رجوع", "callback_data": "account_manager_menu", "style": "danger"}]] # simplified return
        bot.edit_message_text(chat_id=chat_id, message_id=loading_msg.message_id, text=text, parse_mode='HTML', reply_markup=json.dumps({"inline_keyboard": keyboard}))

    # إنشاء حساب واحد
    elif call.data == "create_single":
        loading_msg = bot.send_message(
            chat_id,
            f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري الإنشاء...</b>',
            parse_mode='HTML'
        )
        
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=show_loading_animation, args=(chat_id, loading_msg.message_id, stop_event))
        anim_thread.start()
        
        password = user_data[user_id].get("password", "levi@$618pi")
        result = create_facebook_account(password)
        
        stop_event.set()
        anim_thread.join(timeout=1)
        
        show_account_result(chat_id, loading_msg.message_id, result)
        if result["success"]:
            save_account_to_db(user_id, result)

    # قائمة الإنشاء بالجملة
    elif call.data == "menu_bulk":
        bulk_text = (
            f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji> <b>إنشاء بالجملة</b>\n'
            f'<blockquote>اختر عدد الحسابات التي تريد إنشاءها:</blockquote>'
        )
        
        bulk_keyboard = [
            [
                {
                    "text": "10 حسابات",
                    "callback_data": "bulk_10",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_FIRE
                },
                {
                    "text": "20 حساب",
                    "callback_data": "bulk_20",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_FIRE
                }
            ],
            [
                {
                    "text": "50 حساب",
                    "callback_data": "bulk_50",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_FIRE
                },
                {
                    "text": "عدد مخصص",
                    "callback_data": "bulk_custom",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_SETTINGS
                }
            ],
            [
                {
                    "text": "رجوع",
                    "callback_data": "back_to_start",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_SHIELD
                }
            ]
        ]
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=bulk_text,
            parse_mode='HTML',
            reply_markup=json.dumps({"inline_keyboard": bulk_keyboard})
        )

    # معالجة الإنشاء بالجملة
    elif call.data.startswith("bulk_"):
        if call.data == "bulk_custom":
            user_data[user_id]["state"] = "waiting_custom_count"
            prompt_text = (
                f'<tg-emoji emoji-id="{EMOJI_SETTINGS}">⚙️</tg-emoji> <b>عدد مخصص</b>\n'
                f'<blockquote>أدخل عدد الحسابات التي تريد إنشاءها (1-500):</blockquote>'
            )
            keyboard = [[{"text": "إلغاء", "callback_data": "back_to_start", "style": "danger", "icon_custom_emoji_id": EMOJI_FAIL}]]
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=prompt_text,
                parse_mode='HTML',
                reply_markup=json.dumps({"inline_keyboard": keyboard})
            )
        else:
            count = int(call.data.split('_')[1])
            process_bulk_accounts(chat_id, user_id, count)

    # تغيير الباسورد
    elif call.data == "change_password":
        user_data[user_id]["state"] = "waiting_password"
        prompt_text = (
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> <b>تغيير الباسورد</b>\n'
            f'<blockquote>أرسل الباسورد الجديد:</blockquote>'
        )
        
        keyboard = [[
            {
                "text": "إلغاء",
                "callback_data": "back_to_start",
                "style": "danger",
                "icon_custom_emoji_id": EMOJI_FAIL
            }
        ]]
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=prompt_text,
            parse_mode='HTML',
            reply_markup=json.dumps({"inline_keyboard": keyboard})
        )
    
    # عن المطور
    elif call.data == "about_dev":
        about_text = (
            f'<tg-emoji emoji-id="{EMOJI_DIAMOND}">💎</tg-emoji> <b>المطور</b>\n'
            f'<blockquote expandable>\n'
            f'<b>⎔ الاسم:</b> <a href="https://t.me/Abosgr2024">𝔸𝔹𝕆𝕊𝔾ℝ 𝕐𝔼𝕄𝔼ℕ</a>\n'
            f'<b>⎔ اليوزر:</b> @Abosgr2024\n'
            f'<b>⎔ القناة:</b> https://t.me/+YNZRwbLWXRZjMmVk\n'
            f'</blockquote>\n'
            f'<blockquote expandable>\n'
            f'<b>⚠️ تنبيه هام:</b>\n'
            f'هذه الأداة للأغراض التعليمية فقط.\n'
            f'المطور غير مسؤول عن أي استخدام\n'
            f'خاطئ أو مخالف للقوانين.\n'
            f'تقع المسؤولية الكاملة على المستخدم.\n'
            f'</blockquote>'
        )
        
        keyboard = [[
            {
                "text": "رجوع",
                "callback_data": "back_to_start",
                "style": "danger",
                "icon_custom_emoji_id": EMOJI_SHIELD
            }
        ]]
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=about_text,
            parse_mode='HTML',
            reply_markup=json.dumps({"inline_keyboard": keyboard}),
            disable_web_page_preview=True
        )
    
    # رجوع للرئيسية
    elif call.data == "back_to_start":
        bot.delete_message(chat_id, msg_id)
        send_welcome(call.message)
    
    # إنشاء آخر
    elif call.data == "create_another":
        loading_msg = bot.send_message(
            chat_id,
            f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري الإنشاء...</b>',
            parse_mode='HTML'
        )
        
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=show_loading_animation, args=(chat_id, loading_msg.message_id, stop_event))
        anim_thread.start()
        
        password = user_data[user_id].get("password", "levi@$618pi")
        result = create_facebook_account(password)
        
        stop_event.set()
        anim_thread.join(timeout=1)
        
        show_account_result(chat_id, loading_msg.message_id, result)
        if result["success"]:
            save_account_to_db(user_id, result)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """يعالج الرسائل النصية الواردة من المستخدم."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if user_id not in user_data:
        user_data[user_id] = {"password": "levi@$618pi", "state": "idle"}
    
    state = user_data[user_id].get("state", "idle")
    
    if state == "waiting_password":
        new_pass = message.text.strip()
        user_data[user_id]["password"] = new_pass
        user_data[user_id]["state"] = "idle"
        
        success_text = (
            f'<tg-emoji emoji-id="{EMOJI_SUCCESS}">✅</tg-emoji> <b>تم تحديث الباسورد</b>\n'
            f'<blockquote expandable>الجديد: <code>{new_pass}</code></blockquote>'
        )
        
        keyboard = [[
            {
                "text": "رجوع للرئيسية",
                "callback_data": "back_to_start",
                "style": "danger",
                "icon_custom_emoji_id": EMOJI_SHIELD
            }
        ]]
        
        bot.send_message(
            chat_id,
            success_text,
            parse_mode='HTML',
            reply_markup=json.dumps({"inline_keyboard": keyboard})
        )
    
    elif state == "waiting_custom_count":
        try:
            count = int(message.text.strip())
            if count < 1:
                raise ValueError
            if count > 500:
                count = 500
            
            user_data[user_id]["state"] = "idle"
            process_bulk_accounts(chat_id, user_id, count)
        except:
            error_text = (
                f'<tg-emoji emoji-id="{EMOJI_FAIL}">❌</tg-emoji> <b>خطأ</b>\n'
                f'<blockquote>أدخل رقم صحيح (1-500)</blockquote>'
            )
            bot.send_message(chat_id, error_text, parse_mode='HTML')


print("البوت يعمل الآن...")
bot.infinity_polling()
