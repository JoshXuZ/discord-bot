import aiohttp

URL = "https://www.abcbullion.com.au/store/gold/gmagoldbars1oz-gold-bullion-pool-allocated"

async def get_html():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            response.raise_for_status()
            return await response.text()