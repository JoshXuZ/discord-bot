from discord.ext import commands
from bot.storage import load_json, save_json

COPYPASTAS_FILE = "data/copypastas.json"

class Copypastas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.copypastas = load_json(COPYPASTAS_FILE, {})
    
    def get_list(self, ctx):
        if ctx.guild is None:
            return None
        gid = str(ctx.guild.id)
        if gid not in self.copypastas:
            self.copypastas[gid] = []
        return self.copypastas[gid]
    
    @commands.command()
    async def copypasta(self, ctx):
        import random
        pastas = self.get_list(ctx)

        if pastas == None:
            await ctx.send("This is a server only feature")
            return
        
        if not pastas:
            await ctx.send("This server currently has no copypastas, add one by replying to a message with !addcopypasta")
            return
        
        await ctx.send(random.choice(pastas))
    
    @commands.command()
    async def listcopypastas(self, ctx):
        pastas = self.get_list(ctx)

        if pastas == None:
            await ctx.send("This is a server only feature")
            return
        
        if not pastas:
            await ctx.send("This server currently has no copypastas, add one by replying to a message with !addcopypasta")
            return

        for copy in pastas:
            await ctx.send(copy[:10])
    
    @commands.command()
    async def addcopypasta(self, ctx):
        if ctx.message.reference is None:
            await ctx.reply("Please reply to a message you want me to add.")
            return

        msg = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )

        text = (msg.content or "").strip()
        if not text:
            await ctx.reply("This is not valid")
            return

        pastas = self.get_list(ctx)
        if pastas == None:
            await ctx.send("This is a server only feature")
            return

        if text in pastas:
            await ctx.reply("This is already a copypasta")
            return
        
        pastas.append(text)
        save_json(COPYPASTAS_FILE, self.copypastas)

        await ctx.reply("New copypasta successfully added")
    
    @commands.command()
    async def resetcopypastas(self, ctx):
        pastas = self.get_list(ctx)
        if pastas == None:
            await ctx.send("This is a server only feature")
            return

        pastas.clear()
        save_json(COPYPASTAS_FILE, self.copypastas)

        await ctx.reply("Copypastas have been reset")

async def setup(bot):
    await bot.add_cog(Copypastas(bot))

# [
#   "The Girl you just called fat? She shit herself & lost 15kgs. The Boy you just called stupid? He shit himself. The Girl you just called ugly? She spends hours shitting and farting. The Boy you just tripped? He shit his pants. There`s more to people than you think. Like this if your against bullying.",
#   "I (74M) am finishing up my first term as President of the United States of America. Let me tell you, America is an incredible country, probably one of the best countries in the whole nation. As my reelection comes closer and closer, my opponent Sleepy Joe has been leading in approval ratings, and I began to get worried. Let me tell you, I am the best at being worried. Just ask anybody in my administration, I get worried like no other president. Anyways, I was considering putting Sleepy Joe to sleep for good, which I think is a service not only to his family, but also the nation as a whole. I was going to ask my good pal Putin to borrow some of that poison he’s using to silence the libtards in his country. So Reddit, am I the asshole?",
#   "What the fuck did you just fucking say about me, you little bitch? ",
#   "I'll have you know I graduated top of my class in the Navy Seals...",
#   "I just downvoted your comment.",
#   "FAQ",
#   "What does this mean?",
#   "The amount of karma (points) on your comment and Reddit account has decreased by one.",
#   "Sir, this is a Wendy’s.",
#   "I like your funny words, magic man.",
#   "They hated Jesus because he told them the truth.",
#   "I have to say a lot of people have been asking this question. No, really. A lot of people come up to me and they ask me. They say, 'What's 2+2?' And I tell them look, we know what 2+2 is. We've had almost eight years of the worst kind of math you can imagine. Oh my god, I can't believe it. Addition and subtraction of the 1s the 2s and the 3s. Its terrible. Its just terrible. Look, if you want to know what 2+2 is, do you want to know what 2+2 is? I'll tell you. First of all the number 2, by the way I love the number 2. It's probably my favorite number, no it is my favorite number. You know what, it's probably more like the number two but with a lot of zeros behind it. A lot. If I'm being honest, I mean, if I'm being honest. I like a lot of zeros. Except for Marco Rubio, now he's a zero that I don't like. Though, I probably shouldn't say that. He's a nice guy but he's like, '10101000101', on and on, like that. He's like a computer! You know what I mean? He's like a computer. I don't know. I mean, you know. So, we have all these numbers and we can add them and subtract them and add them. TIMES them even. Did you know that? We can times them OR divide them, they don't tell you that, and I'll tell you, no one is better at the order of operations than me. You wouldn't believe it. That I can tell you. So, we're gonna be the best on 2+2, believe me. OK? Alright. Thank you.",
#   "I LOVE BITCONNECT",
#   "55 BURGERS 55 FRIES 55 TACOS 55 PIES 55 COKES 100 TATER TOTS 100 PIZZA 100 TENDERS 100 MEATBALLS 100 COFFEES 55 WINGS 55 SHAKES 55 PANCAKES 55 PASTAS 55 PASTAS AND 155 TATERS",
#   "Number one. Steady hand. One day, Kim Jong Un need new heart. I do operation. But mistake! Kim Jong Un die! SSD very mad! I hide fishing boat, come to America. No English, no food, no money. Darryl give me job. Now I have house, American car and new woman. Darryl save life.\n\nMy big secret. I kill Kim Jong Un on purpose. I good surgeon. The best!"
# ]