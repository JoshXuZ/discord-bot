from discord.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ensure_voice(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise ValueError("Please join a voice channel first")
        
        return ctx.author.voice.channel

    @commands.command()
    async def join(self, ctx):
        try:
            channel = self.ensure_voice(ctx)
        except ValueError as e:
            await ctx.send(f"**{e}**")
            return
        
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect(cls=wavelink.Player)

        await ctx.send(f"Joined **{channel.name}**")

async def setup(bot):
    await bot.add_cog(Music(bot))