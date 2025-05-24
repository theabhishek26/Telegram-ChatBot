import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
import asyncio
from aiogram import Router

router = Router()

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Config logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@router.message(Command("start", "help"))  # Use Command() instead of commands=[]
async def command_start_handler(message: types.Message):
    """Handles the /start and /help commands."""
    await message.reply("Hello! I'm your echo bot. Send me a message and I'll echo it back to you!\nPowered by Aiogram")

# dp.include_router(router)

@router.message()  # Use Command() instead of commands=[]
async def echo(message: types.Message):
    """This will return echo."""
    await message.reply(message.text)
    
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())