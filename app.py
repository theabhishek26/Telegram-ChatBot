from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from together import Together
import logging
from aiohttp import web
import asyncio
from aiogram import Router
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from queue import Queue
from telegram.ext import CommandHandler


router = Router()
client = Together() 

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

from telegram.ext import CallbackContext



class Reference:
    '''
    A class to store previous response from togetherai.
    '''
    def __init__(self) -> None:
        self.response = ""  # Changed from self.reference to self.response

reference = Reference()
model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

update_queue = Queue()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
# dp = Dispatcher()

# Setup dispatcher
dp = Dispatcher(bot=bot, update_queue=None, use_context=True)

async def health_check(request):
    return web.Response(text="Bot is running")

async def start_web():
    app = web.Application()
    app.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 10000))).start()

async def start_bot():
    await dp.start_polling(bot)

async def main():
    await asyncio.gather(
        start_web(),
        start_bot()
    )

def clear_past():
    """
    This function clears the past conversation history.
    """
    reference.response = ""  # Changed from reference.reference to reference.response

@router.message(Command("clear"))
async def clear(message: types.Message):
    """Handles to clear past conversations and context."""
    clear_past()
    await message.reply("I have cleared the past conversation history. You can start a new conversation now.")

@router.message(Command("start"))
async def command_start_handler(message: types.Message):
    """Handles the /start command."""
    await message.reply("Hello! I'm your Tele bot, created by Freecoil. How can I assist you?")

@router.message(Command("help"))
async def helper(message: types.Message):
    """Handles the /help command."""
    help_command = """
    Hi there! I'm your Tele bot, created by Freecoil. Here are some commands you can use:
    /start - Start the bot and get a welcome message.
    /clear - Clear the conversation history.
    /help - Get help on how to use the bot.
    I hope this helps! If you have any questions, feel free to ask.
    """
    await message.reply(help_command)

@router.message()
async def chat(message: types.Message):
    """Handler that takes user input and returns the response from togetherai."""
    # print(f">>>USER:\n\t{message.text}")
    
    try:
        response = client.chat.completions.create(
            model=model_name,  # Use the variable instead of string "model_name"
            messages=[
                {"role": "assistant", "content": reference.response},  # Fixed typo "assistent" to "assistant"
                {"role": "user", "content": message.text},
            ],
        )
        reference.response = response.choices[0].message.content
        # print(f">>>ASSISTANT:\n\t{reference.response}")
        await message.reply(reference.response)  # Send the actual response instead of static message
    except Exception as e:
        print(f"Error: {e}")
        await message.reply("Sorry, I encountered an error while processing your request.")

dp.include_router(router)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your bot on Render.")

def start(update, context):
    update.message.reply_text("Hello!")

dp.add_handler(CommandHandler("start", start))

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"



async def main():
    await dp.start_polling(bot,skip_updates=False)

if __name__ == '__main__':
    asyncio.run(main())
