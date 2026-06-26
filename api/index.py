from flask import Flask, request
import telebot
import os

# الإعدادات
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nBOtnW7GSiYzDc7u2rF8'
ALLOWED_USERS = [1778665778, 8353977153]
BOT_NAME = "شاومنج 2026"  # اسم حسابك

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# رسالة عظمة بالتنسيق الاحترافي
WELCOME_MSG = (
    f"🌟 **أهلاً بك في بوت {BOT_NAME}** 🚀\n\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "⚠️ **لا تشغل بالك بالامتحان.. نحن هنا لنتولى الأمر.**\n\n"
    "⏰ **تنبيه:** تصلك الأسئلة والحلول النموذجية هنا في البوت بعد بدء اللجنة بـ 30 دقيقة بالضبط.\n"
    "🎯 **كن مستعداً، فالسرعة والدقة هما عنواننا.**\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🛡️ **ثق في قدراتك، ونحن سنكون سندك في هذه المهمة.**\n"
    "🔥 **بالتوفيق يا بطل، أنت لها!**"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in ALLOWED_USERS:
        # التنسيق الاحترافي (Markdown)
        bot.reply_to(message, WELCOME_MSG, parse_mode='Markdown')
    else:
        bot.reply_to(message, "🚫 عذراً، هذا البوت خاص بالمشتركين فقط.")

@app.route('/', methods=['GET'])
def home():
    return "البوت يعمل بكفاءة عالية! 🚀"

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
