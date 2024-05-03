from telethon import TelegramClient, events
import sqlite3
import config
import logging

# Настройка логгирования
from telethon import TelegramClient, events

api_id=24120751
api_hash="acaa33628ae3a74cf956a6826e7779de"
channel = '@mediap2p_chat'  # Указываете нужный канал

# Создаем клиент Telegram
client = TelegramClient('new_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    # Вывод информации о чате и текста сообщения
    print(f"Chat ID: {event.chat_id} Message: {event.message.text}")

async def main():
    await client.start()
    print("Клиент запущен. Ожидание сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
