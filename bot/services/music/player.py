from collections import defaultdict, deque
import asyncio
import discord

class MusicPlayer:
    def __init__(self, bot):
        self.bot = bot
        self.ffmpeg_options = {
            "before_options": (
                "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 "
                "-nostdin -loglevel warning"
            ),
            "options": "-vn -bufsize 5M -maxrate 2M"
        }

        self.queues = defaultdict(deque)
        self.locks = defaultdict(asyncio.Lock)

    def enqueue(self, gid, track):
        self.queues[gid].append(track)

    def enqueue_front(self, gid, track):
        self.queues[gid].appendleft(track)

    def clear_queue(self, gid):
        self.queues[gid].clear()

    def list_queue(self, gid):
        q = list(self.queues[gid])

        embed = discord.Embed(title="🎶 Queue")

        if not q:
            embed.description = "Queue is empty."
            return embed

        lines = [f"**{i+1}.** {t['title']}" for i, t in enumerate(q[:10])]
        embed.description = "\n".join(lines)

        if len(q) > 10:
            embed.set_footer(text=f"+ {len(q) - 10} more")

        return embed

    def play_next(self, gid, vc):
        if not self.queues[gid]:
            return

        track = self.queues[gid].popleft()
        source = discord.FFmpegPCMAudio(track["url"], **self.ffmpeg_options)

        def after(err):
            if err:
                print("Music player error:", err)

            fut = asyncio.run_coroutine_threadsafe(self.play_next_async(gid, vc), self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print("Error scheduling next track:", e)

        vc.play(source, after=after)

    async def play_next_async(self, gid, vc):
        async with self.locks[gid]:
            if not vc or not vc.is_connected():
                return
            if vc.is_playing():
                return
            self.play_next(gid, vc)

    async def start_if_idle(self, gid, vc):
        async with self.locks[gid]:
            if not vc or not vc.is_connected():
                return
            if not vc.is_playing():
                self.play_next(gid, vc)

    async def skip(self, gid, vc):
        if not vc or not vc.is_connected() or not vc.is_playing():
            return False
        vc.stop()
        return True

    async def clear_and_stop(self, gid, vc):
        async with self.locks[gid]:
            self.clear_queue(gid)
            if vc and vc.is_connected() and vc.is_playing():
                vc.stop()