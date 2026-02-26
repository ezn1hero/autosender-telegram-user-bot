#!/usr/bin/env python
import asyncio
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from bot import create_userbot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("userbot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_config() -> dict:
    env_file = Path(__file__).parent / "config.env"
    if not env_file.exists():
        logger.error(f"Файл {env_file} не найден!")
        logger.error("Создайте файл config.env на основе config.env.example")
        raise FileNotFoundError(f"config.env not found")
    
    load_dotenv(env_file)
    
    config = {
        "api_id": int(os.getenv('API_ID', '0')),
        "api_hash": os.getenv('API_HASH'),
        "chat_id": int(os.getenv('CHAT', '0')),
        "password": os.getenv('PASSWORD', None)
    }
    
    missing = []
    if config["api_id"] == 0:
        missing.append("API_ID")
    if not config["api_hash"]:
        missing.append("API_HASH")
    if config["chat_id"] == 0:
        missing.append("CHAT")
    
    if missing:
        error_msg = f"Отсутствуют обязательные переменные: {', '.join(missing)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("Конфигурация загружена успешно")
    logger.info(f"API_ID: {config['api_id']}")
    logger.info(f"CHAT_ID: {config['chat_id']}")
    logger.info(f"2FA пароль: {'установлен' if config['password'] else 'не установлен'}")
    
    return config

def main():
    logger.info("="*50)
    logger.info("Запуск юзер-бота")
    logger.info("="*50)
    
    try:
        config = load_config()
        
        bot = create_userbot(
            api_id=config["api_id"],
            api_hash=config["api_hash"],
            chat_id=config["chat_id"],
            password=config["password"]
        )
        
        asyncio.run(bot.start())
        
    except KeyboardInterrupt:
        logger.info("Юзер-бот остановлен пользователем (Ctrl+C)")
    except FileNotFoundError as e:
        logger.error(f"Ошибка с файлом конфигурации: {e}")
        logger.info("Создайте файл config.env с необходимыми переменными")
        return 1
    except ValueError as e:
        logger.error(f"Ошибка в конфигурации: {e}")
        return 1
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        return 1
    
    logger.info("Юзер-бот завершил работу")
    return 0

if __name__ == "__main__":
    sys.exit(main())