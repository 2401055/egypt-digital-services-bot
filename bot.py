
import telebot
import json
import requests
import random
import time
import re
import threading
import os
from datetime import datetime
from faker import Faker
from bs4 import BeautifulSoup

# Bot token from user input
TOKEN = "8605066160:AAFe8I9wp4RX8-uTsUGU4bfQZJgl4ZwRuv8"
bot = telebot.TeleBot(TOKEN)

# ========== الإيموجيات المتحركة Premium ==========
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

# ========== بيانات المستخدمين ==========
user_data = {}
global_stats = {"created": 0, "failed": 0}

# ========== دوال فيسبوك ==========

def get_regex_group(pattern, text, default_value=""):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return default_value

def get_fake_desktop_ua():
    desktop_uas = [
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "width": 1920,
            "browser": "Chrome",
            "version": "119",
            "full_version_list": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
        },
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "width": 1920,
            "browser": "Chrome",
            "version": "120",
            "full_version_list": '"Google Chrome";v="120", "Chromium";v="120", "Not?A_Brand";v="24"'
        }
    ]
    return random.choice(desktop_uas)

def parse_set_cookie(headers):
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
            if temp:
                temp[-1] += ',' + part.strip()
    for ck in temp:
        kv = ck.split(';', 1)[0]
        if '=' in kv:
            k, v = kv.split('=', 1)
            cookies[k.strip()] = v.strip()
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    return cookies, cookie_str

def create_facebook_account(password=None, first_name=None, last_name=None):
    fake = Faker('en_US')
    ua_data = get_fake_desktop_ua()
    
    if not first_name:
        first_name = fake.first_name()
    if not last_name:
        last_name = fake.last_name()
        
    email_akun = f'{first_name.lower()}{last_name.lower()}{random.randint(100,99999)}@gmail.com'
    if password is None:
        password = 'Pass' + str(random.randint(100000, 999999)) + '@'

    session = requests.Session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': ua_data["full_version_list"],
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': ua_data["ua"],
    }

    try:
        # Step 1: Visit main page
        res1 = session.get('https://www.facebook.com/r.php', headers=headers, timeout=30)
        signup_page = res1.text
        
        # Extract dynamic tokens
        lsd = get_regex_group(r'name="lsd" value="(.*?)"', signup_page)
        jazoest = get_regex_group(r'name="jazoest" value="(.*?)"', signup_page)
        ri = get_regex_group(r'name="ri" value="(.*?)"', signup_page)
        
        # Extra tokens for AJAX
        haste_session = get_regex_group(r'"haste_session":"(.*?)"', signup_page)
        rev = get_regex_group(r'"rev":(\d+)', signup_page)
        hsi = get_regex_group(r'"hsi":"(\d+)"', signup_page)
        spin_t = get_regex_group(r'"__spin_t":(\d+)', signup_page)
        
        if not lsd:
            lsd = "AVo86L310qI" # Fallback but usually extraction is better

        # Step 2: Simulate some delay
        time.sleep(2)
        
        # Step 3: Register
        reg_headers = headers.copy()
        reg_headers.update({
            'origin': 'https://www.facebook.com',
            'referer': 'https://www.facebook.com/r.php',
            'content-type': 'application/x-www-form-urlencoded',
            'x-fb-lsd': lsd,
            'x-asbd-id': '129477',
        })
        
        data = {
            'jazoest': jazoest,
            'lsd': lsd,
            'firstname': first_name,
            'lastname': last_name,
            'birthday_day': str(random.randint(1, 28)),
            'birthday_month': str(random.randint(1, 12)),
            'birthday_year': str(random.randint(1990, 2005)),
            'reg_email__': email_akun,
            'reg_passwd__': password,
            'sex': str(random.randint(1, 2)),
            'ri': ri,
            'action_dialog_shown': '',
            'invid': '',
            'a': '',
            'oi': '',
            'locale': 'en_US',
            'reg_instance': get_regex_group(r'name="reg_instance" value="(.*?)"', signup_page),
            '__user': '0',
            '__a': '1',
            '__req': 'y',
            '__hs': haste_session,
            '__rev': rev,
            '__hsi': hsi,
            '__spin_r': rev,
            '__spin_t': spin_t,
        }

        response = session.post('https://www.facebook.com/ajax/register.php', headers=reg_headers, data=data, timeout=30)
        
        # Check response
        if '"registration_succeeded":true' in response.text:
            cookies = session.cookies.get_dict()
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            return {
                "success": True,
                "first_name": first_name,
                "last_name": last_name,
                "email": email_akun,
                "password": password,
                "cookie": cookie_str
            }
        elif "checkpoint" in response.text or "checkpoint" in response.url:
            return {"success": False, "error": "Checkpoint (الحساب يحتاج تأكيد هوية أو رقم هاتف)"}
        else:
            # Try to extract error message
            error_match = re.search(r'"error_message":"(.*?)"', response.text)
            error_msg = error_match.group(1) if error_match else "فشل التسجيل (قد يكون بسبب الـ IP أو المتصفح)"
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

def check_facebook_account(cookie_str):
    headers = {
        'authority': 'mbasic.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie_str,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    try:
        response = requests.get('https://mbasic.facebook.com/profile.php', headers=headers, timeout=20)
        if "checkpoint" in response.url or "login" in response.url:
            return {"status": "Locked/Checkpoint", "working": False}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('title').text if soup.find('title') else "Unknown"
        
        friends = "0"
        friend_link = soup.find('a', href=re.compile(r'/friends/'))
        if friend_link:
            friends_match = re.search(r'(\d+)', friend_link.text)
            if friends_match:
                friends = friends_match.group(1)
        
        return {
            "status": "Active",
            "working": True,
            "name": name,
            "friends": friends
        }
    except Exception as e:
        return {"status": f"Error: {str(e)}", "working": False}

def perform_fb_post(cookie_str, message="Hello Facebook!"):
    headers = {
        'authority': 'mbasic.facebook.com',
        'cookie': cookie_str,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    try:
        res = requests.get('https://mbasic.facebook.com/', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.find('form', action=re.compile(r'/composer/'))
        if not form:
            return False
        
        action = form['action']
        inputs = form.find_all('input')
        data = {inp.get('name'): inp.get('value') for inp in inputs if inp.get('name')}
        data['xc_message'] = message
        data['view_post'] = 'Post'
        
        requests.post(f'https://mbasic.facebook.com{action}', headers=headers, data=data)
        return True
    except:
        return False

# ========== أوامر البوت ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji> <b>FACEBOOK GEN PRO</b>\n'
        f'<blockquote>أداة إنشاء وإدارة حسابات فيسبوك تلقائياً</blockquote>\n\n'
        f'<blockquote expandable>\n'
        f'<b>⎔ المطور:</b> <a href="https://t.me/Abosgr2024">𝔸𝔹𝕆𝕊𝔾ℝ 𝕐𝔼𝕄𝔼ℕ</a>\n'
        f'</blockquote>'
    )

    keyboard = [
        [
            {"text": "🚀 إنشاء حساب سريع", "callback_data": "create_single"},
            {"text": "👤 إنشاء باسم مخصص", "callback_data": "create_custom_name"}
        ],
        [
            {"text": "🔥 إنشاء بالجملة", "callback_data": "menu_bulk"},
            {"text": "🛠️ مدير الحسابات", "callback_data": "account_manager"}
        ],
        [
            {"text": "🔑 تغيير الباسورد", "callback_data": "change_password"},
            {"text": "💎 عن المطور", "callback_data": "about_dev"}
        ]
    ]

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML',
        reply_markup=json.dumps({"inline_keyboard": keyboard}),
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if user_id not in user_data:
        user_data[user_id] = {"password": None, "state": "idle"}
    
    if call.data == "back_to_start":
        send_welcome(call.message)
        bot.delete_message(chat_id, msg_id)
        return

    if call.data == "create_single":
        bot.send_message(chat_id, "⏳ جاري محاولة إنشاء حساب... قد يستغرق الأمر لحظات.")
        result = create_facebook_account(user_data[user_id]["password"])
        show_account_result(chat_id, result)

    elif call.data == "create_custom_name":
        user_data[user_id]["state"] = "waiting_first_name"
        bot.send_message(chat_id, "👤 حسناً، أرسل الآن **الاسم الأول** الذي تريده:")

    elif call.data == "account_manager":
        bot.send_message(chat_id, "🛠️ **مدير الحسابات**\nأرسل الكوكيز الخاصة بالحساب لفحصه أو تنفيذ مهام عليه:")
        user_data[user_id]["state"] = "waiting_cookies"

    elif call.data == "menu_bulk":
        user_data[user_id]["state"] = "waiting_custom_count"
        bot.send_message(chat_id, "🔢 كم عدد الحسابات التي تريد إنشاؤها؟ (1-5)")

    elif call.data == "change_password":
        user_data[user_id]["state"] = "waiting_password"
        bot.send_message(chat_id, "🔑 أرسل الباسورد الجديد:")

    elif call.data == "about_dev":
        bot.send_message(chat_id, "💎 مطور البوت: @Abosgr2024\nقناة التحديثات: @Abosgr_yemen")

def show_account_result(chat_id, result):
    if result["success"]:
        text = (
            f"✅ **تم إنشاء الحساب بنجاح!**\n\n"
            f"👤 **الاسم:** `{result['first_name']} {result['last_name']}`\n"
            f"📧 **الإيميل:** `{result['email']}`\n"
            f"🔒 **الباسورد:** `{result['password']}`\n"
            f"🍪 **الكوكيز:**\n`{result['cookie']}`"
        )
        with open('accounts.txt', 'a') as f:
            f.write(f"{result['email']}|{result['password']}|{result['cookie']}\n")
    else:
        text = (
            f"❌ **فشل الإنشاء**\n\n"
            f"⚠️ **السبب:** {result['error']}\n\n"
            f"💡 **نصيحة:** فيسبوك يفرض قيوداً صارمة على الـ IP. إذا استمرت المشكلة، حاول استخدام بروكسي أو تغيير الـ IP الخاص بك."
        )
    
    bot.send_message(chat_id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if user_id not in user_data:
        user_data[user_id] = {"password": None, "state": "idle"}
        
    state = user_data[user_id].get("state", "idle")

    if state == "waiting_first_name":
        user_data[user_id]["custom_first"] = message.text.strip()
        user_data[user_id]["state"] = "waiting_last_name"
        bot.send_message(chat_id, "✅ تمام، الآن أرسل **اسم العائلة**:")

    elif state == "waiting_last_name":
        last_name = message.text.strip()
        first_name = user_data[user_id]["custom_first"]
        user_data[user_id]["state"] = "idle"
        bot.send_message(chat_id, f"⏳ جاري محاولة إنشاء حساب باسم: {first_name} {last_name}...")
        result = create_facebook_account(user_data[user_id]["password"], first_name, last_name)
        show_account_result(chat_id, result)

    elif state == "waiting_cookies":
        cookies = message.text.strip()
        user_data[user_id]["state"] = "idle"
        bot.send_message(chat_id, "🔍 جاري فحص الحساب...")
        info = check_facebook_account(cookies)
        
        if info["working"]:
            res_text = (
                f"✅ **الحساب يعمل!**\n\n"
                f"👤 **الاسم الحقيقي:** {info['name']}\n"
                f"👥 **الأصدقاء:** {info['friends']}\n"
                f"📊 **الحالة:** {info['status']}\n\n"
                f"تلميح: يمكنك الآن النشر لتقوية الحساب."
            )
            if perform_fb_post(cookies, "صباح الخير، حساب جديد هنا!"):
                res_text += "\n\n🚀 **تم نشر منشور ترحيبي تلقائياً لتقوية الحساب!**"
        else:
            res_text = f"❌ **الحساب معطل أو الكوكيز غير صالحة.**\nالحالة: {info['status']}"
        
        bot.send_message(chat_id, res_text, parse_mode='Markdown')

    elif state == "waiting_password":
        user_data[user_id]["password"] = message.text.strip()
        user_data[user_id]["state"] = "idle"
        bot.send_message(chat_id, "✅ تم تحديث الباسورد الافتراضي.")

    elif state == "waiting_custom_count":
        try:
            count = int(message.text.strip())
            if 1 <= count <= 5:
                user_data[user_id]["state"] = "idle"
                bot.send_message(chat_id, f"⏳ جاري محاولة إنشاء {count} حسابات... يرجى الانتظار.")
                for i in range(count):
                    result = create_facebook_account(user_data[user_id]["password"])
                    show_account_result(chat_id, result)
                    if i < count - 1:
                        time.sleep(10)
            else:
                bot.send_message(chat_id, "⚠️ الرجاء إدخال رقم بين 1 و 5 لتجنب الحظر السريع.")
        except:
            bot.send_message(chat_id, "⚠️ الرجاء إدخال رقم صحيح.")

if __name__ == "__main__":
    print("Bot is starting with optimized registration flow...")
    bot.infinity_polling()
