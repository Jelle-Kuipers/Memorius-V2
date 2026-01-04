import discord
import os
from dotenv import load_dotenv
from utils.database import init_db
from bot_actions.on_guild import on_guild_join, on_guild_remove
import config.logger as logger

# Set up intents
intents = discord.Intents.default()
intents.guilds = True

# Initialize bot
bot = discord.Bot(intents=intents)
load_dotenv()
TOKEN = str(os.getenv("TOKEN"))

# Initialize database
init_db()

# Register all commands from commands folder
commands_dir = "commands"
for filename in os.listdir(commands_dir):
    if filename.endswith(".py"):
        module_name = filename[:-3]
        module = __import__(f"{commands_dir}.{module_name}", fromlist=[""])
        # Assuming each command file has a setup function to add commands to the bot
        if hasattr(module, "setup"):
            module.setup(bot)

# Register bot actions
bot_actions_dir = "bot_actions"
for filename in os.listdir(bot_actions_dir):
    if filename.endswith(".py"):
        module_name = filename[:-3]
        module = __import__(f"{bot_actions_dir}.{module_name}", fromlist=[""])
        # Assuming each bot action file has functions to register events
        for attr in dir(module):
            func = getattr(module, attr)
            if callable(func) and attr.startswith("on_"):
                event_name = attr[3:]  # Remove 'on_' prefix
                bot.event(func)

# Run bot
bot.run(TOKEN)