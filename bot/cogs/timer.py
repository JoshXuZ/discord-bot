from discord.ext import commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.countdown_tasks = {}
    
    @commands.command()
    async def countdown(self, ctx, arg=None):
        if not arg or not arg.isdigit():
            await ctx.reply("Please enter a valid number")
            return
        
        timer = int(arg)

        if ctx.guild.id in self.countdown_tasks:
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
                self.countdown_tasks.pop(ctx.guild.id, None)
        
        task = asyncio.create_task(run())
        self.countdown_tasks[ctx.guild.id] = task

    @commands.command()
    async def stop(self, ctx):
        task = self.countdown_tasks.get(ctx.guild.id)
        if not task:
            await ctx.reply("There is no countdown to stop")
            return
        
        task.cancel()

async def setup(bot):
    await bot.add_cog(Timer(bot))