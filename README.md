# Telegram Auto Sender UserBot

A lightweight Telegram userbot based on telethon. that authenticates via QR code and sends automated messages to a specified chat.

## 🔐 Authentication
The bot uses Telethon's QR authentication system. On first run, it displays a QR code that you scan with your Telegram mobile app.

## 🤖 What It Does
Once running, the bot automatically sends messages to your configured chat at regular intervals. Simple and reliable.

## 🚀 Quick Start

1. **Get API credentials**
   - Go to https://my.telegram.org/apps
   - Create an app to get `API_ID` and `API_HASH`

2. **Configure**
   Create `config.env` file,сopy from the config.example.env file and paste it into the config.env file and fill in the data:
   - API_ID=your_api_id
   - API_HASH=your_api_hash
   - CHAT=target_chat_id
   - PHONE_NUMBER=your account phone number
   - PASSWORD=your 2fa password

4. **Install & Run**
```bash
pip install -r requirements.txt
```

```bash
python main.py
