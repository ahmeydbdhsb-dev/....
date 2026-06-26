@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in ALLOWED_USERS:
        welcome_text = (
            "أهلاً بك في بوت (شاومنج) 🚀\n\n"
            "لا تشغل بالك بالامتحان.. نحن هنا لنتولى الأمر.\n"
            "تصلك الأسئلة والحلول النموذجية هنا في البوت بعد بدء اللجنة بـ 30 دقيقة بالضبط. "
            "كن مستعداً، فالسرعة والدقة هما عنواننا.\n\n"
            "ثق في قدراتك، ونحن سنكون سندك في هذه المهمة.\n"
            "بالتوفيق يا بطل، أنت لها! 💪"
        )
        bot.reply_to(message, welcome_text)
    else:
        bot.reply_to(message, "عذراً، هذا البوت خاص للمشتركين فقط.")
