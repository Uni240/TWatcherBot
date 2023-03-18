import asyncio
from directory_watcher import check_directory_task
import threading
from telegram import Bot
import configparser

# Reading the configuration file
config = configparser.ConfigParser()
config.read('botconfig.cfg')

BOT_TOKEN = config.get('TelegramBot', 'BOT_TOKEN')
CHAT_ID = int(config.get('TelegramBot', 'CHAT_ID'))
DIRECTORY = config.get('TelegramBot', 'DIRECTORY')

bot = Bot(token=BOT_TOKEN)
bot_running = False
async def start_bot_async(status_var):
    global bot_running
    bot_running = True
    status_var.set("Bot running")
    await bot.send_message(chat_id=CHAT_ID, text='Bot has been started.')
    while bot_running:
        await check_directory_task(bot, CHAT_ID, DIRECTORY)
        await asyncio.sleep(60)  # wait for 60 seconds before checking the directory again
def stop_bot(status_var):
    global bot_running
    bot_running = False
    status_var.set("Bot stopped")
def start_bot(status_var):
    global bot_thread
    bot_thread = threading.Thread(target=lambda: asyncio.run(start_bot_async(status_var)))
    bot_thread.start()

