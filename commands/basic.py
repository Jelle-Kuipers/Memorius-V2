# Basic commands (Hello, ping etc.)
import random
from utils.flavour_text_loader import ping

def setup(bot):
    @bot.slash_command()
    async def hello(ctx, name: str = None):
        name = name or ctx.author.name
        await ctx.respond(f"Hello {name}!")

    @bot.slash_command(guild_ids=[1157633750310596618])  # Replace with your guild ID for testing
    async def latency(ctx):
        delay = bot.latency * 1000  # Convert to milliseconds
        text = random.choice(ping.flavour_texts)
        await ctx.respond(text.format(delay=f"{delay:.2f}"))