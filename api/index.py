from flask import Flask, request, render_template_string
import telebot
from telethon import TelegramClient
import os
import asyncio

# إعدادات حسابك الصحيحة والمؤكدة بالتنشيط
API_ID = 30478732
API_HASH = '394d6d66d2097791253e89282b6f4318'
# التوكن الصحيح والمفعّل (يحتوي على حرف O الكابيتال)
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nBOtnW7GSiYzDc7u2rF8'
TARGET_CHANNEL = 'shaksbb'
ALLOWED_USERS = [1778665778, 8353977153]

# تفادي تضارب مكتبات تليجرام على فيرسيل لتجنب AttributeError
try:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
except AttributeError:
    import sys
    sys.modules['telebot'] = __import__('telebot')
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

app = Flask(__name__)

# مسار ملف الـ Session السحرية
SESSION_PATH = os.path.join(os.path.dirname(__file__), '..', 'vercel_session.session')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>بوابة بوت شاومنج</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; direction: rtl; }
        .card { background: white; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); max-width: 90%; width: 400px; margin-top: 50px; }
        .status { padding: 15px; background: #e2f0d9; color: #385723; border-radius: 6px; font-size: 16px; font-weight: bold; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="color: #28a745;">تم تفعيل البوت بنجاح! ✅</h2>
        <p style="color: #666; font-size: 14px;">السيرفر متصل الآن بملف الجلسة والتوكن الصحيح ومستعد لإرسال الصور فوراً.</p>
        <div class="status">الحالة: مستقر وجاهز للعمل 🚀</div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/cron', methods=['GET'])
def cron_job():
    if not os.path.exists(SESSION_PATH):
        return f"Session file missing", 400
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    
    async def run():
        await client.connect()
        if await client.is_user_authorized():
            # سحب آخر رسالة من القناة المستهدفة
            messages = await client.get_messages(TARGET_CHANNEL, limit=1)
            if messages and messages[0].photo:
                # تحميل الصورة في المجلد المؤقت المسموح به على فيرسيل لتجنب أخطاء الـ Read-only
                temp_photo_path = '/tmp/temp_photo.jpg'
                await client.download_media(messages[0].photo, temp_photo_path)
                
                if os.path.exists(temp_photo_path):
                    for user_id in ALLOWED_USERS:
                        try:
                            with open(temp_photo_path, 'rb') as photo_file:
                                bot.send_photo(user_id, photo_file, caption=messages[0].text)
                        except Exception:
                            pass
                    # مسح الملف المؤقت فوراً
                    try:
                        os.remove(temp_photo_path)
                    except Exception:
                        pass
        await client.disconnect()

    loop.run_until_complete(run())
    return "Cron checked successfully and messages sent!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid request", 403
