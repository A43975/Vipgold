import os
import telebot

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

bot = telebot.TeleBot(TOKEN)

# سيتم تسجيل القنوات التي يصل منها منشور
channel_ids = set()


@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    source_channel = message.chat.id

    # تسجيل القناة التي جاء منها المنشور
    channel_ids.add(source_channel)

    # نسخ المنشور إلى كل القنوات التي عرفها البوت
    for channel_id in list(channel_ids):
        if channel_id == source_channel:
            continue

        try:
            bot.copy_message(
                chat_id=channel_id,
                from_chat_id=source_channel,
                message_id=message.message_id
            )
        except Exception as e:
            print(f"Error copying to {channel_id}: {e}")


print("Bot is running...")
bot.infinity_polling(
    allowed_updates=["channel_post"]
)
