import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from dotenv import load_dotenv
from aiohttp import web
from together import Together

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

# Initialize Together API client
client = Together()
model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Aiogram bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

class Reference:
    """
    A class to store previous response from Together.ai.
    """
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

# Health check endpoint
async def health_check(request):
    return web.Response(text="Bot is running")

# Define command handlers
@router.message(Command("start"))
async def command_start_handler(message: types.Message):
    await message.reply("Hello! I'm your Tele bot, created by Freecoil. How can I assist you?")

@router.message(Command("help"))
async def helper(message: types.Message):
    help_text = (
        "Hi there! I'm your Tele bot, created by Freecoil. Here are some commands you can use:\n"
        "/start - Start the bot and get a welcome message.\n"
        "/clear - Clear the conversation history.\n"
        "/help - Get help on how to use the bot."
    )
    await message.reply(help_text)

@router.message(Command("clear"))
async def clear(message: types.Message):
    reference.response = ""
    await message.reply("I have cleared the past conversation history. You can start a new conversation now.")

@router.message()
async def chat(message: types.Message):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "assistant", "content": reference.response},
                {"role": "user", "content": message.text},
            ],
        )
        reference.response = response.choices[0].message.content
        await message.reply(reference.response)
    except Exception as e:
        print(f"Error: {e}")
        await message.reply("Sorry, I encountered an error while processing your request.")

# Include router into dispatcher
dp.include_router(router)

# Start both webhook (health) and polling concurrently
async def main():
    app = web.Application()
    app.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Health check running at http://0.0.0.0:{PORT}/")

    # Start bot polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
