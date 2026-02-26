import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import os
import qrcode

load_dotenv('config.env')

api_id = int(os.getenv('API_ID', '0'))
api_hash = os.getenv('API_HASH')
chat = int(os.getenv('CHAT'))
password = os.getenv('PASSWORD')

client = TelegramClient("qr_session", api_id, api_hash)


async def qr_auth():
    await client.connect()

    if await client.is_user_authorized():
        print("Найдена сессия")
        return
    
    qr_login = await client.qr_login()

    qr = qrcode.QRCode()
    qr.add_data(qr_login.url)
    qr.print_ascii(invert=True)

    try:
        await qr_login.wait()
    except SessionPasswordNeededError:
        await client.sign_in(password=password)
    print("Успешная авторизация!")


async def send_fish():
    while True:
        await client.send_message(chat, "фиш")
        print(f"[{datetime.now()}] Отправлено: фиш")
        await asyncio.sleep(600)


async def send_daily_commands():
    while True:
        now = datetime.now()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if now >= next_run:
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        await client.send_message(chat, "/grow")
        await asyncio.sleep(2)
        await client.send_message(chat, "/net")

        print(f"[{datetime.now()}] Отправлены: /grow и /net")


async def main():
    await qr_auth()
    print("Запущено")

    await asyncio.gather(
        send_fish(),
        send_daily_commands(),
        )


asyncio.run(main())