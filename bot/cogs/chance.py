from discord.ext import commands
import random

class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def coinflip(self, ctx, arg=None):
        coin = "heads"
        if random.randint(0, 1):
            coin = "tails"

        await ctx.reply(f"The coin landed {coin}")

    @commands.command()
    async def dice(self, ctx):
        await ctx.reply(f"The dice landed on {random.randint(1, 6)}")
        
    @commands.command()
    async def card(self, ctx):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Spades", "Diamonds", "Clubs", "Hearts"]

        rank = random.choice(ranks)
        suit = random.choice(suits)

        await ctx.reply(f"You drew the {rank} of {suit}")

async def setup(bot):
    await bot.add_cog(Chance(bot))