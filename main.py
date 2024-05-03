from telethon import TelegramClient, events
import sqlite3
import config
import logging

api_id = 24120751  # Замените на ваш API ID
api_hash = 'acaa33628ae3a74cf956a6826e7779de'  # Замените на ваш API Hash

# Настройка логгирования
client = TelegramClient('new_session2', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    logging.info(f"Received message from {event.chat_id}: {event.text}")

async def main():
    await client.start()  # Теперь требуется ввести номер телефона
    print("Клиент запущен. Ожидание сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
