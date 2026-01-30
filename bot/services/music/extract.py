import asyncio
import yt_dlp

class YTDLPExtractor:
    def __init__(self):
        self.ytdlp = yt_dlp.YoutubeDL({
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch",
        })

    async def extract_track(self, query):
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdlp.extract_info(query, download=False))

        if "entries" in data:
            data = data["entries"][0]

        return {
            "title": data.get("title", "Unknown title"),
            "url": data["url"],   # direct stream URL
        }