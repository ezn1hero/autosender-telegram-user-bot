import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import qrcode
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FishUserBot:
    
    def __init__(self, api_id: int, api_hash: str, chat_id: int, password: Optional[str] = None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.chat_id = chat_id
        self.password = password
        self.client = TelegramClient("qr_session", api_id, api_hash)
        self._running = False
    
    async def qr_auth(self) -> bool:
        await self.client.connect()
        
        if await self.client.is_user_authorized():
            logger.info("Найдена существующая сессия")
            return True
        
        logger.info("Запуск QR-авторизации")
        qr_login = await self.client.qr_login()
        
        qr = qrcode.QRCode()
        qr.add_data(qr_login.url)
        print("\n" + "="*50)
        print("Отсканируйте qr-код для входа аккаунт")
        print("="*50)
        qr.print_ascii(invert=True)
        print("="*50 + "\n")
        
        try:
            await qr_login.wait()
            logger.info("QR-код подтвержден")
        except SessionPasswordNeededError:
            if self.password:
                await self.client.sign_in(password=self.password)
                logger.info("Вход выполнен")
            else:
                logger.error("Требуется пароль для 2FA")
                return False
        
        logger.info("Успешная авторизация!")
        return True
    
    async def send_fish(self):
        logger.info("Текущая задача: Отправка фиш")
        while self._running:
            try:
                await self.client.send_message(self.chat_id, "фиш")
                logger.info(f"[{datetime.now()}] Отправлено: фиш")
                await asyncio.sleep(600)
            except Exception as e:
                logger.error(f"Ошибка при отправке 'фиш': {e}")
                await asyncio.sleep(60)
    
    async def send_daily_commands(self):
        logger.info("Текущая задача: отправка /grow, /net")
        while self._running:
            try:
                now = datetime.now()
                
                next_run = now.replace(hour=3, minute=4, second=0, microsecond=0)
                if now >= next_run:
                    next_run += timedelta(days=1)
                
                wait_seconds = (next_run - now).total_seconds()
                logger.info(f"До следующей отправки команд: {wait_seconds/3600:.1f} часов")
                await asyncio.sleep(wait_seconds)
                
                await self.client.send_message(self.chat_id, "/grow")
                logger.info(f"[{datetime.now()}] Отправлено: /grow")
                await asyncio.sleep(2)
                
                await self.client.send_message(self.chat_id, "/net")
                logger.info(f"[{datetime.now()}] Отправлено: /net")
                
            except Exception as e:
                logger.error(f"Ошибка при отправке команд: {e}")
                await asyncio.sleep(60)
    
    async def start(self):
        logger.info("="*50)
        logger.info("Запуск")
        logger.info("="*50)
        
        if not await self.qr_auth():
            logger.error("Не удалось авторизоваться")
            return
        
        me = await self.client.get_me()
        logger.info(f"Авторизован как: {me.first_name} (@{me.username})")
        logger.info(f"ID: {me.id}")
        logger.info(f"Чат для отправки: {self.chat_id}")
        
        self._running = True
        logger.info("Запуск задач...")
        
        try:
            await asyncio.gather(
                self.send_fish(),
                self.send_daily_commands(),
            )
        except asyncio.CancelledError:
            logger.info("Задачи остановлены")
        finally:
            self._running = False
            await self.stop()
    
    async def stop(self):
        logger.info("Остановка")
        self._running = False
        await self.client.disconnect()
        logger.info("Юзер-бот остановлен")

userbot = None

def create_userbot(api_id: int, api_hash: str, chat_id: int, password: str = None):
    global userbot
    userbot = FishUserBot(api_id, api_hash, chat_id, password)
    return userbot