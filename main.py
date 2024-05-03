from telethon import TelegramClient, events
import sqlite3
import config
import logging

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    # Создание клиента Telegram
    client = TelegramClient('new_session', config.api_id, config.api_hash)
    logging.info('Клиент Telegram успешно создан')
except Exception as e:
    logging.error(f'Ошибка при создании клиента Telegram: {e}')

@client.on(events.NewMessage(chats=config.channel_usernames))
async def handler(event):
    try:
        user_id = event.sender_id
        # Получаем информацию о чате
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', 'некий чат')  # Получаем название чата или используем 'некий чат' по умолчанию
        message_text = event.message.text if event.message else 'Сообщение без текста'  # Получаем текст сообщения или стандартное сообщение

        cursor.execute('SELECT user_id FROM messaged_users WHERE user_id = ?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO messaged_users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            logging.info(f'Новый пользователь {user_id} добавлен в базу данных')
            try:
                # Отправляем сообщение с информацией о новом пользователе, названии чата и тексте сообщения
                await client.send_message(-4095716021, f'Пользователь с ID {user_id} впервые написал в чат "{chat_title}": {message_text}')
                logging.info(f'Сообщение о новом пользователе {user_id} отправлено')
            except Exception as e:
                logging.error(f'Ошибка при отправке сообщения о новом пользователе {user_id}: {e}')
    except Exception as e:
        logging.error(f'Ошибка при обработке нового сообщения: {e}')


async def main():
    try:
        await client.start()
        for channel in config.channel_usernames:
            logging.info("CHANNEL IS " + channel)
        logging.info('Клиент Telegram успешно запущен')
        await client.run_until_disconnected()
    except Exception as e:
        logging.error(f'Ошибка при запуске клиента Telegram: {e}')
    finally:
        conn.close()
        logging.info('Соединение с базой данных SQLite закрыто')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
