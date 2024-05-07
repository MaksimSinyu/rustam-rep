from telethon import TelegramClient, events, sync
import logging
import sqlite3
import config

logging.basicConfig(level=logging.DEBUG)

try:
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messaged_users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    logging.info('База данных SQLite успешно инициализирована')
except Exception as e:
    logging.error(f'Ошибка при инициализации базы данных SQLite: {e}')

try:
    # Создание клиента Telegram один раз
    client = TelegramClient('dsa8yday8das8ydd', config.api_id, config.api_hash)
    logging.info('Клиент Telegram успешно создан')
except Exception as e:
    logging.error(f'Ошибка при создании клиента Telegram: {e}')

@client.on(events.NewMessage(chats=config.channel_usernames))
async def handler(event):
    try:
        logging.info("NEW MESSAGE")
        # Использование get_sender_id(), если доступно, для устранения проблем с sender_id
        user_id = await event.get_sender_id()
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', 'некий чат')
        message_text = event.message.text if event.message else 'Сообщение без текста'

        cursor.execute('SELECT user_id FROM messaged_users WHERE user_id = ?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO messaged_users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            logging.info(f'Новый пользователь {user_id} добавлен в базу данных')

            user_link = f"[Пользователь с ID {user_id}](tg://user?id={user_id})"
            message_content = f'{user_link} впервые написал в чат "{chat_title}": {message_text}'
            
            # Используйте chat_id из конфигурации или предопределенный
            await client.send_message(config.log_chat_id, message_content, parse_mode='md')
            logging.info(f'Сообщение о новом пользователе {user_id} отправлено')
    except Exception as e:
        logging.error(f'Ошибка при обработке нового сообщения: {e}')

async def main():
    await client.start()
    await client.catch_up()
    logging.info("Client started. Listening for new messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
