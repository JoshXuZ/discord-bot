from discord.ext import commands
import asyncio
from bot.services.music.extract import YTDLPExtractor
from bot.services.music.player import MusicPlayer

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = MusicPlayer(bot)
        self.extractor = YTDLPExtractor()

    async def ensure_voice(self, ctx):
        if not ctx.guild:
            raise ValueError("This is a server only command")

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise ValueError("Please join a voice channel first")
        
        channel = ctx.author.voice.channel
        vc = ctx.voice_client

        if vc and vc.is_connected():
            if vc.channel != channel:
                await vc.move_to(channel)
            return vc

        return await channel.connect()

    @commands.command()
    async def join(self, ctx: commands.Context):
        try:
            vc = await self.ensure_voice(ctx)
        except ValueError as e:
            return await ctx.send(f"**{e}**")

        if vc:
            await ctx.send(f"Joined **{vc.channel}**")

    @commands.command()
    async def playnow(self, ctx, *, query):
        try:
            vc = await self.ensure_voice(ctx)
        except ValueError as e:
            return await ctx.send(f"**{e}**")

        async with ctx.typing():
            try:
                track = await self.extractor.extract_track(query)
            except Exception:
                return await ctx.send("Couldn't load that track. Try another link/search.")
        
        gid = ctx.guild.id
        self.player.enqueue_front(gid, track)
        await ctx.send(f"Now playing: **{track['title']}**")

        if vc.is_playing():
            vc.stop()
        else:
            await self.player.start_if_idle(gid, vc)
    
    @commands.command()
    async def queue(self, ctx, *, query=None):
        try:
            vc = await self.ensure_voice(ctx)
        except ValueError as e:
            return await ctx.send(f"**{e}**")
        
        gid = ctx.guild.id

        if not query:
            return await ctx.send(embed=self.player.list_queue(gid))

        async with ctx.typing():
            try:
                track = await self.extractor.extract_track(query)
            except Exception:
                return await ctx.send("Couldn't load that track. Try another link/search.")

        self.player.enqueue(gid, track)
        await ctx.send(f"Queued: **{track['title']}**")
        await self.player.start_if_idle(gid, vc)
    
    @commands.command()
    async def playnext(self, ctx, *, query=None):
        try:
            vc = await self.ensure_voice(ctx)
        except ValueError as e:
            return await ctx.send(f"**{e}**")
        
        gid = ctx.guild.id

        if not query:
            return await ctx.send("Please enter a song you want to add")

        async with ctx.typing():
            try:
                track = await self.extractor.extract_track(query)
            except Exception:
                return await ctx.send("Couldn't load that track. Try another link/search.")

        self.player.enqueue_front(gid, track)
        await ctx.send(f"Next up: **{track['title']}**")
        await self.player.start_if_idle(gid, vc)

    @commands.command()
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("I'm not in a voice channel.")

        ok = await self.player.skip(ctx.guild.id, vc)
        await ctx.send("Skipped." if ok else "Nothing is playing.")

    @commands.command()
    async def clearqueue(self, ctx):
        gid = ctx.guild.id
        vc = ctx.voice_client
        await self.player.clear_and_stop(gid, vc)
        await ctx.send("Queue cleared.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        guild = member.guild
        vc = guild.voice_client

        if not vc or not vc.is_connected():
            return

        channel = vc.channel

        await asyncio.sleep(10)
        if vc.is_connected() and len(channel.members) == 1:
            self.player.clear_queue(guild.id)
            await vc.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))