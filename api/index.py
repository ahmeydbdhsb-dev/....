from flask import Flask, request, render_template_string
import telebot
from telethon import TelegramClient
import requests
import asyncio

API_ID = 30478732
API_HASH = '394d6d66d2097791253e89282b6f4318'
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nB0tnW7GSiYzDc7u2rF8'
TARGET_CHANNEL = 'shaksbb'
ALLOWED_USERS = [1778665778, 8353977153]

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/shawmng-ba277/databases/(default)/documents/auth/telegram"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>تفعيل بوت شاومنج</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="text-align:center; font-family:Arial, sans-serif; padding:20px; background:#f4f4f4; direction: rtl;">
    <div style="background:white; padding:30px; border-radius:12px; display:inline-block; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); max-width: 90%; width: 400px; margin-top: 50px;">
        <h2 style="color: #333;">لوحة تحكم بوت شاومنج 🚀</h2>
        <p style="color: #666; font-size: 14px;">أدخل رقمك واستقبل كود تليجرام لتشغيل المراقبة فوراً على فيرسيل</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        
        <form method="POST">
            <input type="text" name="phone" placeholder="اكتب رقم الهاتف (+20...)" required style="padding:12px; width:90%; margin-bottom:15px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px;"><br>
            <input type="text" name="code" placeholder="اكتب كود تليجرام (إذا وصلك)" style="padding:12px; width:90%; margin-bottom:20px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px;"><br>
            <button type="submit" style="padding:12px 25px; background:#28a745; color:white; border:none; border-radius: 6px; font-size: 16px; cursor:pointer; width: 95%;">تفعيل وحفظ البيانات</button>
        </form>
        
        {% if msg %}
            <div style="margin-top:20px; padding:10px; background:#e2f0d9; color:#385723; border-radius:6px; font-size: 14px;">
                {{ msg }}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    msg = ""
    if request.method == 'POST':
        phone = request.form.get('phone')
        code = request.form.get('code')
        
        if phone and not code:
            payload = {"fields": {"phone": {"stringValue": phone}, "status": {"stringValue": "request_code"}}}
            requests.patch(FIRESTORE_URL, json=payload)
            msg = f"تم حفظ الرقم {phone}. انتظر دقيقة واحدة وسيصلك كود تليجرام، ثم اكتبه بالأسفل."
        elif code:
            payload = {"fields": {"code": {"stringValue": code}, "status": {"stringValue": "verify_code"}}}
            requests.patch(FIRESTORE_URL, json=payload)
            msg = "جاري تفعيل الكود الآن... تفقد البوت الخاص بك بعد دقيقة."
            
    return render_template_string(HTML_TEMPLATE, msg=msg)

# الموتور التلقائي اللي فيرسيل هيشغله كل دقيقة في الخلفية لطلب الكود والمراقبة
@app.route('/api/cron', methods=['GET'])
def cron_job():
    res = requests.get(FIRESTORE_URL).json()
    if 'fields' not in res:
        return "No data", 200
        
    fields = res['fields']
    status = fields.get('status', {}).get('stringValue', '')
    phone = fields.get('phone', {}).get('stringValue', '')
    
    # استخدام Telethon بشكل سريع لطلب الكود أو المراقبة
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('vercel_session', API_ID, API_HASH)
    
    async def run():
        await client.connect()
        if status == "request_code":
            # طلب الكود من تليجرام وإرساله لهاتفك
            await client.send_code_request(phone)
            payload = {"fields": {"phone": {"stringValue": phone}, "status": {"stringValue": "waiting_code"}}}
            requests.patch(FIRESTORE_URL, json=payload)
            
        elif status == "verify_code":
            # إدخال الكود وتفعيل الحساب
            code = fields.get('code', {}).get('stringValue', '')
            await client.sign_in(phone, code)
            payload = {"fields": {"status": {"stringValue": "running"}}}
            requests.patch(FIRESTORE_URL, json=payload)
            
        elif status == "running":
            # فحص آخر رسالة بالقناة وسحب الصور
            messages = await client.get_messages(TARGET_CHANNEL, limit=1)
            if messages and messages[0].photo:
                # إرسال الصورة لكل المشتركين عبر تليجرام بوت API مباشرة
                for user_id in ALLOWED_USERS:
                    bot.send_photo(user_id, messages[0].photo, caption=messages[0].text)
                    
        await client.disconnect()

    loop.run_until_complete(run())
    return "Cron executed", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
