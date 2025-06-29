from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import asyncio
import datetime
import time

# Настройки
API_ID = 28455545  # Замените на ваш API ID
API_HASH = '8558523fe78561ac521f42860fdaecf9'  # Замените на ваш API HASH
PHONE_NUMBER = '+79870995363'  # Ваш номер телефона
SESSION_NAME = 'userbot_session'

# Каналы для мониторинга (username или ID)
TARGET_CHANNELS = ['@PodarokDurova']

# Ваш комментарий
COMMENT_TEXT = "ogo"

# Ваш ID для отправки уведомлений (можно узнать у бота @userinfobot)
YOUR_USER_ID = 7677719551

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    print("Юзербот запущен и мониторит каналы...")
    
    @client.on(events.NewMessage(chats=TARGET_CHANNELS))
    async def handler(event):
        # Проверяем, что это пост (а не комментарий или другое сообщение)
        if not event.is_channel or event.is_group:
            return
            
        post = event.message
        post_time = post.date
        
        # Засекаем время перед отправкой комментария
        start_time = time.time()
        
        try:
            # Отправляем комментарий
            await client.send_message(
                entity=event.chat_id,
                message=COMMENT_TEXT,
                comment_to=post.id
            )
            
            # Рассчитываем время выполнения
            end_time = time.time()
            reaction_time = end_time - start_time
            time_since_post = (datetime.datetime.now(datetime.timezone.utc) - post_time).total_seconds()
            
            # Отправляем себе отчет
            report = (
                f"📊 Отчет о комментарии\n\n"
                f"🔗 Канал: {event.chat.title or event.chat_id}\n"
                f"🕒 Время публикации поста: {post_time}\n"
                f"⏱ Время реакции: {reaction_time:.2f} сек\n"
                f"⏳ Время с момента публикации: {time_since_post:.2f} сек\n"
                f"📝 Комментарий: {COMMENT_TEXT}"
            )
            
            await client.send_message(YOUR_USER_ID, report)
            
        except Exception as e:
            error_msg = f"❌ Ошибка при комментировании: {str(e)}"
            await client.send_message(YOUR_USER_ID, error_msg)
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())