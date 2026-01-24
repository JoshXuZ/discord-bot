from discord.ext import commands
from bot.services.elements.factory import get_provider, list_provider
from bot.services.elements.client import get_html
import aiohttp
import discord


class metals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def price(self, ctx, metal='gold'):
        metal = metal.lower()              

        provider = get_provider(metal)
        if not provider:
            await ctx.send("Please enter a valid metal")
            return
        
        try:
            html = await get_html()
            await ctx.send(f"Current {metal} price:\n{provider.calculate(html)} per oz")
        except aiohttp.ClientError:
            await ctx.send("Network error while fetching the gold price.")
        except discord.HTTPException as e:
            await ctx.send(f"Discord send failed: `{e}`")
        except ValueError as e:
            await ctx.send(f"Parse error: **{e}**")

    @commands.command()
    async def list_metals(self, ctx):
        metals = list_provider()
        desc = "\n".join(f"• **{m.title()}** (`!price {m}`)" for m in metals)

        embed = discord.Embed(title="Metals", description=desc)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(metals(bot))
