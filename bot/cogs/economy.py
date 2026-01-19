from discord.ext import commands
from bot.storage import load_json, save_json
import random

BAL_FILE = "data/balances.json"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balance = load_json(BAL_FILE, {})
    
    @commands.command()
    async def bal(self, ctx):
        user_id = str(ctx.author.id)
        amount = int(self.balance.get(user_id, 0))
        self.balance[user_id] = amount
        save_json(BAL_FILE, self.balance)

        if amount == 0:
            await ctx.reply(f"{ctx.author} is broke, *everyone laugh at this user*")
        else:
            await ctx.reply(f"{ctx.author} has {amount} in their balance")

    @commands.command()
    async def beg(self, ctx):
        user_id = str(ctx.author.id)
        amount = random.randint(0, 5)
        self.balance[user_id] = int(self.balance.get(user_id, 0) + amount)
        save_json(BAL_FILE, self.balance)

        if amount == 0:
            await ctx.reply(f"{ctx.author} couldn't even beg properly")
        else:
            await ctx.reply(f"{ctx.author} managed to beg {amount}\nTheir balance is now {self.balance[user_id]}")

async def setup(bot):
    await bot.add_cog(Economy(bot))