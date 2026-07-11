
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
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "width": 1920,
            "browser": "Microsoft Edge",
            "version": "138",
            "full_version_list": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Microsoft Edge";v="138.0.3351.121"'
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

def create_facebook_account(password=None):
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
        response = requests.get('https://www.facebook.com/?_rdc=1&_rdr', cookies=cookies, headers=headers, timeout=30)
        cookies.update(dict(response.cookies.get_dict()))
        headers.update({'referer': 'https://www.facebook.com/?_rdc=1&_rdr'})
        
        signup_resp = requests.get('https://www.facebook.com/r.php?entry_point=login', cookies=cookies, headers=headers, timeout=30)
        signup = signup_resp.text.replace('\\', '')
        
        lsd_token = 'AVo86L310qI'
        haste_session = get_regex_group('"haste_session":"(.*?)"', signup)
        ccg = get_regex_group('"connectionClass":"(.*?)"', signup)
        rev = get_regex_group(r'"consistency":{"rev":(\d+)', signup)
        hsi = get_regex_group(r'"hsi":"(\d+)"', signup)
        spint = get_regex_group(r'"__spin_t":(\d+)', signup)
        vip = get_regex_group('"vip":"(.*?)"', signup)
        
        headers.update({'x-asbd-id': '359341', 'x-fb-lsd': lsd_token})

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

        response = requests.post('https://web.facebook.com/ajax/register.php', headers=headers, data=data, timeout=30)

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
            return {"success": False, "error": "Registration failed or checkpoint"}
    except Exception as e:
        return {"success": False, "error": str(e)}

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

def show_loading_animation(chat_id, msg_id, stop_event):
    frames = ["▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰"]
    i = 0
    while not stop_event.is_set():
        frame = frames[i % len(frames)]
        text = (
            f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري المعالجة...</b>\n'
            f'<blockquote>[{frame}]</blockquote>'
        )
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=text, parse_mode='HTML')
        except: pass
        i += 1
        time.sleep(0.8)

# ========== أوامر البوت ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji> <b>FACEBOOK GEN</b>\n'
        f'<blockquote>أداة إنشاء حسابات فيسبوك تلقائياً</blockquote>\n\n'
        f'<blockquote expandable>\n'
        f'<b>⎔ المطور:</b> <a href="https://t.me/Abosgr2024">𝔸𝔹𝕆𝕊𝔾ℝ 𝕐𝔼𝕄𝔼ℕ</a>\n'
        f'</blockquote>'
    )

    keyboard = [
        [{"text": "إنشاء حساب", "callback_data": "create_single", "style": "success", "icon_custom_emoji_id": EMOJI_ROCKET}],
        [{"text": "إنشاء بالجملة", "callback_data": "menu_bulk", "style": "primary", "icon_custom_emoji_id": EMOJI_FIRE},
         {"text": "مدير الحسابات", "callback_data": "account_manager", "style": "primary", "icon_custom_emoji_id": EMOJI_USER}],
        [{"text": "تغيير الباسورد", "callback_data": "change_password", "style": "primary", "icon_custom_emoji_id": EMOJI_KEY},
         {"text": "عن المطور", "callback_data": "about_dev", "style": "primary", "icon_custom_emoji_id": EMOJI_DIAMOND}]
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
        user_data[user_id] = {"password": "levi@$618pi", "state": "idle"}
    
    if call.data == "create_single":
        loading_msg = bot.send_message(chat_id, f'<tg-emoji emoji-id="{EMOJI_LOADING}">⏳</tg-emoji> <b>جاري الإنشاء...</b>', parse_mode='HTML')
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=show_loading_animation, args=(chat_id, loading_msg.message_id, stop_event))
        anim_thread.start()
        
        result = create_facebook_account(user_data[user_id]["password"])
        stop_event.set()
        anim_thread.join(timeout=1)
        show_account_result(chat_id, loading_msg.message_id, result)

    elif call.data == "account_manager":
        bot.send_message(chat_id, "🛠️ **مدير الحسابات**\nأرسل الكوكيز الخاصة بالحساب لفحصه أو تنفيذ مهام عليه:")
        user_data[user_id]["state"] = "waiting_cookies"

    elif call.data == "menu_bulk":
        bot.send_message(chat_id, "🔢 كم عدد الحسابات التي تريد إنشاؤها؟ (1-10)")
        user_data[user_id]["state"] = "waiting_custom_count"

    elif call.data == "change_password":
        bot.send_message(chat_id, "🔑 أرسل الباسورد الجديد:")
        user_data[user_id]["state"] = "waiting_password"

    elif call.data == "about_dev":
        bot.send_message(chat_id, "💎 مطور البوت: @Abosgr2024\nقناة التحديثات: @Abosgr_yemen")

    elif call.data == "back_to_start":
        send_welcome(call.message)
        bot.delete_message(chat_id, msg_id)

def show_account_result(chat_id, msg_id, result):
    if result["success"]:
        text = (
            f'<tg-emoji emoji-id="{EMOJI_SUCCESS}">✅</tg-emoji> <b>تم الإنشاء بنجاح</b>\n'
            f'<blockquote expandable>\n'
            f'<b>👤 الاسم:</b> <code>{result["first_name"]} {result["last_name"]}</code>\n'
            f'<b>📧 الإيميل:</b> <code>{result["email"]}</code>\n'
            f'<b>🔒 الباسورد:</b> <code>{result["password"]}</code>\n'
            f'<b>🍪 الكوكيز:</b>\n<code>{result["cookie"]}</code>\n'
            f'</blockquote>'
        )
    else:
        text = f'<tg-emoji emoji-id="{EMOJI_FAIL}">❌</tg-emoji> <b>فشل الإنشاء</b>\n<blockquote>{result["error"]}</blockquote>'
    
    keyboard = [[{"text": "رجوع", "callback_data": "back_to_start", "style": "danger", "icon_custom_emoji_id": EMOJI_SHIELD}]]
    bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=text, parse_mode='HTML', reply_markup=json.dumps({"inline_keyboard": keyboard}))

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    state = user_data.get(user_id, {}).get("state", "idle")

    if state == "waiting_cookies":
        cookies = message.text.strip()
        user_data[user_id]["state"] = "idle"
        bot.send_message(chat_id, "🔍 جاري فحص الحساب...")
        info = check_facebook_account(cookies)
        
        if info["working"]:
            res_text = (
                f"✅ **الحساب يعمل!**\n\n"
                f"👤 **الاسم الحقيقي:** {info['name']}\n"
                f"👥 **الأصدقاء:** {info['friends']}\n"
                f"📊 **الحالة:** {info['status']}\n"
            )
            if perform_fb_post(cookies, "صباح الخير، حساب جديد هنا!"):
                res_text += "\n🚀 **تم نشر منشور ترحيبي تلقائياً لتقوية الحساب!**"
        else:
            res_text = f"❌ **الحساب معطل أو الكوكيز غير صالحة.**\nالحالة: {info['status']}"
        bot.send_message(chat_id, res_text)

    elif state == "waiting_password":
        user_data[user_id]["password"] = message.text.strip()
        user_data[user_id]["state"] = "idle"
        bot.send_message(chat_id, "✅ تم تحديث الباسورد الافتراضي.")

    elif state == "waiting_custom_count":
        try:
            count = int(message.text.strip())
            if 1 <= count <= 10:
                user_data[user_id]["state"] = "idle"
                bot.send_message(chat_id, f"⏳ جاري إنشاء {count} حسابات...")
                for i in range(count):
                    result = create_facebook_account(user_data[user_id]["password"])
                    if result["success"]:
                        bot.send_message(chat_id, f"✅ تم إنشاء حساب {i+1}")
                    else:
                        bot.send_message(chat_id, f"❌ فشل إنشاء حساب {i+1}")
                    time.sleep(5)
            else:
                bot.send_message(chat_id, "⚠️ أدخل رقم بين 1 و 10.")
        except:
            bot.send_message(chat_id, "⚠️ أدخل رقم صحيح.")

if __name__ == "__main__":
    bot.infinity_polling()
