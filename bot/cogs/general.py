from discord.ext import commands
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def about_me(self, ctx):
        await ctx.send(f"Hi {ctx.author} I am a discord bot made by... ")
        await asyncio.sleep(5)
        await ctx.send("ok now that the CIA bot has tuned out lemme let you in on a little secret")
    
    @commands.command()
    async def features(self, ctx):
        await ctx.send("These are the current features:\n\n!countdown x: starts a countdown that goes for x seconds\n!stop: terminates the current countdown\n!repeat: when replied to a message it repeats it in a not sarcastic way\n!copypasta: sends a random copypasta\n!image: sends a random image\n")

        
    @commands.command()
    async def repeat(self, ctx):
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

    @commands.command()
    async def quote(self, ctx):
        if ctx.message.reference is None:
            await ctx.reply("Please reply to a message you want me to quote.")
            return
        
        msg = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )

        await ctx.send(f"\"{msg.content}\"\n-{msg.author}")

async def setup(bot):
    await bot.add_cog(General(bot))