from telethon import TelegramClient, events
import sqlite3
import config
import logging

# Настройка логгирования
client = TelegramClient('new_session2', config.api_id, config.api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    logging.info(f"Received message from {event.chat_id}: {event.text}")

async def main():
    await client.start()  # Теперь требуется ввести номер телефона
    print("Клиент запущен. Ожидание сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
