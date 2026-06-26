from flask import Flask, request, render_template_string
import telebot
import os

# الإعدادات: ضع الـ ID الخاص بك هنا
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nBOtnW7GSiYzDc7u2rF8'
ALLOWED_USERS = [1778665778, 8353977153]

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# رسالة الترحيب "العظمة"
WELCOME_MSG = (
    "أهلاً بك في بوت شاومنج 🚀\n\n"
    "لا تشغل بالك بالامتحان.. نحن هنا لنتولى الأمر.\n"
    "تصلك الأسئلة والحلول النموذجية هنا في البوت بعد بدء اللجنة بـ 30 دقيقة بالضبط. "
    "كن مستعداً، فالسرعة والدقة هما عنواننا.\n\n"
    "ثق في قدراتك، ونحن سنكون سندك في هذه المهمة.\n"
    "بالتوفيق يا بطل، أنت لها! 💪"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in ALLOWED_USERS:
        bot.reply_to(message, WELCOME_MSG)
    else:
        bot.reply_to(message, "عذراً، هذا البوت خاص للمشتركين فقط. للتواصل يرجى مراجعة المسؤول.")

@app.route('/', methods=['GET'])
def home():
    return "البوت يعمل بكفاءة! ✅"

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid request", 403

if __name__ == "__main__":
    app.run()
