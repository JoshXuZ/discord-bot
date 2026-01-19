import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# load cogs
INITIAL_EXTENSIONS = [
    "bot.cogs.economy",
    "bot.cogs.copypastas",
    "bot.cogs.general",
    "bot.cogs.chance",
    "bot.cogs.timer",
    "bot.cogs.images",
    "bot.cogs.metals"
]

@bot.event
async def on_ready():
    print("Bot ready:", bot.user)

async def setup():
    for ext in INITIAL_EXTENSIONS:
        await bot.load_extension(ext)

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)