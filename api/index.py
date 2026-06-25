from flask import Flask, request, render_template_string
import telebot
import requests

# 1. إعدادات تليجرام (الجاهزة بتاعتك)
API_ID = 30478732
API_HASH = '394d6d66d2097791253e89282b6f4318'
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nB0tnW7GSiYzDc7u2rF8'

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# رابط الـ REST API المباشر للفايرستور الخاص بمشروعك
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
            # إرسال البيانات للفايرستور عبر الـ REST API مباشرة
            payload = {
                "fields": {
                    "phone": {"stringValue": phone},
                    "status": {"stringValue": "waiting_code"}
                }
            }
            requests.patch(FIRESTORE_URL, json=payload)
            msg = f"تم إرسال الرقم {phone} بنجاح. اطلب الكود الآن من تليجرام واكتبه في الخانة بالأسفل."
        elif code:
            # تحديث الكود في الفايرستور
            payload = {
                "fields": {
                    "phone": {"stringValue": phone if phone else ""},
                    "code": {"stringValue": code},
                    "status": {"stringValue": "done"}
                }
            }
            requests.patch(FIRESTORE_URL, json=payload)
            msg = "تم تحديث كود التفعيل بنجاح! السيرفر سيبدأ المراقبة الآن."
            
    return render_template_string(HTML_TEMPLATE, msg=msg)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
