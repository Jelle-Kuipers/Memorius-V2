import discord
import os
from dotenv import load_dotenv
from utils.database import init_db


# Initialize bot
bot = discord.Bot()
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

# Run bot
bot.run(TOKEN)