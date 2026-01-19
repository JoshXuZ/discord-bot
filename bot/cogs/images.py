import discord
from discord.ext import commands
import random
from data.images.images import IMAGE_PATHS

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.images = IMAGE_PATHS

    @commands.command()
    async def image(self, ctx):
        await ctx.send(file=discord.File(random.choice(self.images)))
    
    @commands.command()
    async def slideshow(self, ctx, arg=None):
        if arg and not arg.isdigit():
            await ctx.send("Please choose a valid number")
            return

        if not arg or int(arg) > len(self.images):
            for paths in self.images:
                await ctx.send(file=discord.File(paths))
            
            return
      
        res = random.sample(range(0, len(self.images)), int(arg))
        for num in res:
            await ctx.send(file=discord.File(self.images[num]))

    @commands.command()
    async def addimage(self, ctx):
        if not ctx.message.reference:
            await ctx.send("Please reply to an image")
            return
        
        replied = ctx.message.reference.resolved

        if not replied:
            await ctx.send("Something went wrong")
            return

        url = filename = None

        if replied.attachments:
            attached = replied.attachments[0]
            url = attached.url
            filename = attached.filename
        
        
async def setup(bot):
    await bot.add_cog(Images(bot))