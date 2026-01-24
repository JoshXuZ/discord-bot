from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def bal(self, ctx):
        try:
            amount = self.bot.bank.bal(ctx.author.id, ctx.guild.id if ctx.guild else None)
        except ValueError as e:
            await ctx.reply(str(e))  # "This is a server only feature"
            return

        if amount == 0:
            await ctx.reply(f"{ctx.author} is broke, *everyone laugh at this user*")
        else:
            await ctx.reply(f"{ctx.author} has {amount} in their balance")

    @commands.command()
    async def beg(self, ctx):
        gid = ctx.guild.id if ctx.guild else None
        if gid is None:
            await ctx.reply("This is a server only feature.")
            return

        amount = random.randint(0, 5)
        new_bal = self.bot.bank.deposit(ctx.author.id, gid, amount)

        if amount == 0:
            await ctx.reply(f"{ctx.author} couldn't even beg properly")
        else:
            await ctx.reply(f"{ctx.author} managed to beg {amount}\nTheir balance is now {new_bal}")


async def setup(bot):
    await bot.add_cog(Economy(bot))