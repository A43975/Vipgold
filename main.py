import os
import telebot

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SOURCE_CHANNEL = os.environ["SOURCE_CHANNEL_ID"]

TARGET_CHANNELS = [
    channel.strip()
    for channel in os.environ["TARGET_CHANNEL_IDS"].split(",")
    if channel.strip()
]

bot = telebot.TeleBot(TOKEN)


@bot.channel_post_handler(
    func=lambda message: str(message.chat.id) == SOURCE_CHANNEL
)
def copy_post(message):
    for channel in TARGET_CHANNELS:
        try:
            bot.copy_message(
                chat_id=channel,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            print(f"Copied successfully to {channel}")

        except Exception as error:
            print(f"Failed to copy to {channel}: {error}")


print("Bot is running...")

bot.infinity_polling(
    allowed_updates=["channel_post"]
)
