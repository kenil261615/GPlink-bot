from os import environ
import aiohttp
from pyrogram import Client, filters
import pickledb

db = pickledb.load('pickle.db', True)

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')

bot = Client('linkshortify bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm Linkshortify bot. Just send me link and get short link")

@bot.on_message(filters.command('set') & filters.private)
async def set(bot, message):
  if len(message.command) > 1:
    db.set(message.from_user.id, message.command[1])
    await message.reply('Set')

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link, db.get(message.from_user.id))
        await message.reply(f'Here is your [short link]({short_link})', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link, api_key):
    url = 'https://linkshortify.com/api'
    params = {'api': api_key, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
