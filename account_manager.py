import requests
import re
import json
import time

def get_headers(cookies_str):
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
    headers = get_headers(cookies_str)
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
    headers = get_headers(cookies_str)
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
    # هذه الوظائف تتطلب FB_DTSG و JAZOEST للقيام بعمليات النشر
    headers = get_headers(cookies_str)
    try:
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
