from discord.ext import commands
from bot.services.gaming.games import flip_coin, roll_dice, draw_card

class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_server(self, ctx):
        if ctx.guild is None:
            raise ValueError("Server-only command. Use this in a server.")
        
        return ctx.author.id, ctx.guild.id

    async def rungame(self, ctx, wager, call, resolver, label):
        try:
            uid, gid = self.check_server(ctx)
            outcome, multiplier, wager = resolver(wager, call)
            self.bot.bank.can_afford(uid, gid, wager)
        except ValueError as e:
            await ctx.send(f"**{e}**")
            return

        bal = self.bot.bank.manage_fund(uid, gid, wager, multiplier)
        await ctx.reply(f"The {label} landed on **{outcome}**. Your balance is now **{bal}**.")

    @commands.command()
    async def coinflip(self, ctx, wager=None, call=None):
        await self.rungame(ctx, wager, call, flip_coin, "coin")

    @commands.command()
    async def dice(self, ctx, wager=None, call=None):
        await self.rungame(ctx, wager, call, roll_dice, "dice")
        
    @commands.command()
    async def card(self, ctx, wager=None, call=None):
        await self.rungame(ctx, wager, call, draw_card, "card")

async def setup(bot):
    await bot.add_cog(Chance(bot))