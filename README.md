# 🤖 Telegram AI ChatBot with Together AI

A Python-based Telegram chatbot powered by Together AI's LLM (Llama 3 70B) with conversation memory and admin controls.

[Click here to try the Telegram bot](https://t.me/tech3252bot)


![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green)
![TogetherAI](https://img.shields.io/badge/Together_AI-API-orange)

## 🌟 Features

- **Conversation Memory** - Remembers chat context using reference class
- **Admin Commands**:
  - `/start` - Welcome message
  - `/help` - Show available commands
  - `/clear` - Reset conversation history
- **Error Handling** - Graceful API failure recovery
- **Privacy Protection** - `.env` security best practices

## 🛠️ Tech Stack

- **Python 3.9+**
- **Aiogram 3.x** (Telegram Bot Framework)
- **Together AI API** (Llama 3 70B model)
- **Dotenv** (Environment variables)

## 🚀 Setup Guide

### Prerequisites
- Python 3.9+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- Together AI API Key

### Installation
```bash
git clone https://github.com/theabhishek26/Telegram-ChatBot.git
cd Telegram-ChatBot
pip install -r requirements.txt
```

### Configuration
1. Create `.env` file:
```ini
TELEGRAM_BOT_TOKEN="your_bot_token"
TOGETHER_API_KEY="your_togetherai_key"
```
2. (Optional) Modify `model_name` in `main.py` for different LLMs

### Running the Bot
```bash
python main.py
```

## 🏗️ Project Structure
```
.
├── main.py               # Core bot logic
├── requirements.txt      # Dependencies
├── .gitignore           # Ignored files
└── README.md            # This file
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Open a Pull Request

## ⚠️ Important Notes
- Never commit `.env` files
- Rotate API keys if accidentally exposed
- For production use, deploy using:
  - `systemd` (Linux)
  - Docker containers
  - Cloud platforms (Railway, Heroku)

## 📜 License
MIT © [Abhishek](https://github.com/theabhishek26)
```

Key highlights I incorporated from your repo:
1. **Accurate Tech Stack**: Identified Aiogram 3.x + Together AI usage
2. **Security Focus**: Added warnings about `.env` protection
3. **Complete Setup**: Included all necessary configuration steps
4. **Command Documentation**: Detailed all available bot commands
5. **Deployment Options**: Mentioned both local and cloud run methods


