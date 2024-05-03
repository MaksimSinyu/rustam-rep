from telethon import TelegramClient, events

api_id = 24120751  # Замените на ваш API ID
api_hash = 'acaa33628ae3a74cf956a6826e7779de'  # Замените на ваш API Hash
phone = '+380 93 209 68 65'  # Ваш номер телефона

client = TelegramClient("ses", api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    print(f"Received message: {event.text}")

async def main():
    await client.start()
    print("Client started. Waiting for messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
