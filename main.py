import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
import asyncio
import random
from copypastas import COPYPASTAS
from images.images import IMAGE_PATHS

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
countdown_tasks = {}

@bot.event
async def on_ready():
    print("Lock and loaded", bot.user.name)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     print("not sent by bot")
#     await message.channel.send(f"Woah ruuuuuuuuuude, {message.author.mention}")
#     await bot.process_commands(message)

@bot.command()
async def about_me(ctx):
    await ctx.send(f"Hi {ctx.author} I am a discord bot made by... ")
    await asyncio.sleep(5)
    await ctx.send("ok now that the CIA bot has tuned out lemme let you in on a little secret")

@bot.command()
async def reply(ctx):
    print("I have been called")
    await ctx.reply("I hate it here please kick me from the server")

@bot.command()
async def features(ctx):
    await ctx.send("These are the current features:\n\n!countdown x: starts a countdown that goes for x seconds\n!stop: terminates the current countdown\n!repeat: when replied to a message it repeats it in a not sarcastic way\n!copypasta: sends a random copypasta\n!image: sends a random image\n")

@bot.command()
async def countdown(ctx, arg=None):
    if not arg or not arg.isdigit():
        await ctx.reply("Please enter a valid number")
        return
    
    timer = int(arg)

    if ctx.guild.id in countdown_tasks:
        await ctx.reply("A countdown is already running")
        return

    async def run():
        try:
            for i in range(timer, 0, -1):
                await ctx.send(f"{i}")
                await asyncio.sleep(1)
            await ctx.reply("The countdown has finished")
        except asyncio.CancelledError:
            await ctx.send("The timer has been cancelled")
        finally:
            countdown_tasks.pop(ctx.guild.id, None)
    
    task = asyncio.create_task(run())
    countdown_tasks[ctx.guild.id] = task

@bot.command()
async def stop(ctx):
    task = countdown_tasks.get(ctx.guild.id)
    if not task:
        await ctx.reply("There is no countdown to stop")
        return
    
    task.cancel()

@bot.command()
async def repeat(ctx):
    # Check if the command message is a reply
    if ctx.message.reference is None:
        await ctx.reply("Please reply to a message you want me to repeat.")
        return

    # Fetch the original message
    replied_message = await ctx.channel.fetch_message(
        ctx.message.reference.message_id
    )

    result = []
    upper = True

    for ch in replied_message.content:
        if ch.isalpha():
            result.append(ch.upper() if upper else ch.lower())
            upper = not upper
        else:
            result.append(ch)

    await ctx.reply("".join(result))

@bot.command()
async def copypasta(ctx):
    await ctx.send(random.choice(COPYPASTAS))

@bot.command()
async def image(ctx):
    await ctx.send(file=discord.File(random.choice(IMAGE_PATHS)))

@bot.command()
async def coinflip(ctx):
    coin = "heads"
    if random.randint(0, 1):
        coin = "tails"

    await ctx.reply(f"The coin landed {coin}")

@bot.command()
async def dice(ctx):
    await ctx.reply(f"The dice landed on {random.randint(1, 6)}")

@bot.command()
async def card(ctx):
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["Spades", "Diamonds", "Clubs", "Hearts"]

    rank = random.choice(ranks)
    suit = random.choice(suits)

    await ctx.reply(f"You drew the {rank} of {suit}")

@bot.command()
async def quote(ctx):
    if ctx.message.reference is None:
        await ctx.reply("Please reply to a message you want me to quote.")
        return
    
    msg = await ctx.channel.fetch_message(
        ctx.message.reference.message_id
    )

    await ctx.send(f"\"{msg.content}\"\n-{msg.author}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
