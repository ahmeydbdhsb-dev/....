from telethon import TelegramClient, events

# 1. بيانات حسابك الشخصي (تم إدخالها من صورك)
API_ID = 30478732
API_HASH = '394d6d66d2097791253e89282b6f4318'

# 2. توكن البوت (تم إدخاله من صورتك)
BOT_TOKEN = '8668088040:AAE3DVD67ZitM04nB0tnW7GSiYzDc7u2rF8'

# 3. يوزر نيم قناة التسريبات المستهدفة
TARGET_CHANNEL = 'shaksbb' 

# 4. قائمة الـ IDs المسموح لها بالاشتراك
ALLOWED_USERS = {1778665778, 8353977153}

# قائمة حفظ المشتركين النشطين
active_subscribers = set()

# تشغيل الـ Userbot والـ Bot معاً
user_client = TelegramClient('user_session', API_ID, API_HASH)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

# [جزء البوت] - الترحيب بالمشتركين المسموحين فقط
@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.chat_id
    
    if user_id in ALLOWED_USERS:
        active_subscribers.add(user_id)
        
        sender = await event.get_sender()
        first_name = sender.first_name if sender.first_name else "يا بطل"
        
        welcome_text = (
            f"أهلاً بك يا {first_name}! 👋\n\n"
            "متلقلقش الامتحان هيكون محلول بعديها بأقل من 30 دقيقة، "
            "وهيكون مبعوت هنا وهو محلول من أكبر نخب المدرسين."
        )
        await event.reply(welcome_text)
    else:
        await event.reply("عذراً، هذا البوت خاص ومغلق حالياً.")

# [جزء الحساب الشخصي] - مراقبة القناة وسحب الصور فقط تلقائياً
@user_client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def channel_handler(event):
    if event.message.photo:
        for user_id in active_subscribers:
            try:
                await bot_client.send_file(user_id, event.message.photo, caption=event.message.text)
            except Exception as e:
                print(f"فشل الإرسال للمستخدم {user_id}: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print("البوت شغال حالياً ويراقب القناة بنجاح...")
    await user_client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
