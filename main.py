from telethon import TelegramClient, events, sync
import logging

logging.basicConfig(level=logging.DEBUG)

api_id = 24120751
api_hash = 'acaa33628ae3a74cf956a6826e7779de'
phone = '+380 93 209 68 65'

client = TelegramClient("sesassadsasads1", api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    print(f"Received message: {event.text}")

async def main():
    await client.start()
    await client.catch_up()  # Подписаться на обновления в реальном времени
    print("Client started. Listening for new messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
