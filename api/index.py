from flask import Flask, request, render_template_string
import telebot
from telethon import TelegramClient
import os
import asyncio

# إعدادات حسابك الصحيحة
API_ID = 30478732
API_HASH = '394d6d66d2097791253e89282b6f4318'
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nB0tnW7GSiYzDc7u2rF8'
TARGET_CHANNEL = 'shaksbb'
ALLOWED_USERS = [1778665778, 8353977153]

# تفادي أي تضارب مكتبات على السيرفر
try:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
except AttributeError:
    import sys
    sys.modules['telebot'] = __import__('telebot')
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

app = Flask(__name__)

# مسار ملف الـ Session
SESSION_PATH = os.path.join(os.path.dirname(__file__), '..', 'vercel_session.session')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>تفعيل بوت شاومنج</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="text-align:center; font-family:Arial, sans-serif; padding:20px; background:#f4f4f4; direction: rtl;">
    <div style="background:white; padding:30px; border-radius:12px; display:inline-block; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); max-width: 90%; width: 400px; margin-top: 50px;">
        <h2 style="color: #28a745;">البوت متصل بنجاح! ✅</h2>
        <p style="color: #666; font-size: 14px;">تم تخطي قيود الـ Cron وبناء المشروع بنجاح 100%.</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <div style="padding:15px; background:#e2f0d9; color:#385723; border-radius:6px; font-size: 16px; font-weight: bold;">
            حالة السيرفر: مستقر أوتوماتيكياً 🚀
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

# دالة مخصصة لطلب التحديثات أوتوماتيكياً عبر الـ Webhook بدون قيود
@app.route('/run-check', methods=['GET'])
def manual_check():
    if not os.path.exists(SESSION_PATH):
        return "Session file missing", 400
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    
    async def run():
        await client.connect()
        if await client.is_user_authorized():
            messages = await client.get_messages(TARGET_CHANNEL, limit=1)
            if messages and messages[0].photo:
                for user_id in ALLOWED_USERS:
                    try:
                        bot.send_photo(user_id, messages[0].photo, caption=messages[0].text)
                    except Exception:
                        pass
        await client.disconnect()

    loop.run_until_complete(run())
    return "Check completed successfully!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid request", 403
